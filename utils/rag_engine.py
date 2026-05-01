import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict, Optional
import json
import os
import numpy as np
from datetime import datetime

class AdvancedRAGEngine:
    """
    Advanced RAG engine with:
    - Better embedding model (all-mpnet-base-v2 - 768 dimensions)
    - Dynamic weighted scoring
    - Re-ranking capabilities
    - Multi-field support
    """
    
    def __init__(self, model_name: str = 'all-mpnet-base-v2', use_reranker: bool = True):
        """Initialize with advanced model"""
        
        print(f"Loading embedding model: {model_name}...")
        # Better model: 768 dimensions, 86.9% accuracy (vs 82.4% for MiniLM)
        self.embedding_model = SentenceTransformer(model_name)
        
        # Optional: Cross-encoder for re-ranking (more accurate but slower)
        self.use_reranker = use_reranker
        if use_reranker:
            print("Loading re-ranker model...")
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        # Setup ChromaDB
        os.makedirs("./data/chroma_db", exist_ok=True)
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        
        # Create/get collection
        try:
            self.collection = self.client.get_collection("cvs_advanced")
        except:
            self.collection = self.client.create_collection("cvs_advanced")
        
        print("RAG Engine ready!")
    
    def add_cv(self, cv_data: Dict, field: str = "Software Engineering"):
        """Add CV with comprehensive indexing"""
        
        # Create rich text representation for embedding
        cv_text = self._create_comprehensive_text(cv_data)
        
        # Generate embedding (768 dimensions)
        embedding = self.embedding_model.encode(cv_text).tolist()
        
        # Prepare metadata (all searchable fields)
        metadata = {
            'name': cv_data['name'],
            'field': field,
            'email': cv_data['email'],
            'phone': cv_data['phone'],
            'location': cv_data.get('location', 'Not specified'),
            'linkedin': cv_data.get('linkedin', 'Not provided'),
            'github': cv_data.get('github', 'Not provided'),
            
            # Structured data (JSON serialized)
            'skills': json.dumps(cv_data['skills']),
            'certifications': json.dumps(cv_data.get('certifications', [])),
            'licenses': json.dumps(cv_data.get('licenses', [])),
            'languages': json.dumps(cv_data.get('languages', [])),
            
            # Text sections
            'education': cv_data.get('education', 'Not specified'),
            'experience': cv_data.get('experience', 'Not specified'),
            'projects': cv_data.get('projects', 'No projects listed'),
            'achievements': cv_data.get('achievements', 'No achievements listed'),
            'summary': cv_data.get('summary', ''),
            
            # Calculated fields
            'years_of_experience': str(cv_data.get('years_of_experience', 0)),
            'experience_level': cv_data.get('experience_level', 'Unknown'),
            'education_level': cv_data.get('education_level', 'Not specified'),
            
            # Metadata
            'filename': cv_data['filename'],
            'processed_date': cv_data.get('processed_date', datetime.now().isoformat())
        }
        
        # Store in vector database
        try:
            self.collection.upsert(
                ids=[cv_data['filename']],
                embeddings=[embedding],
                documents=[cv_text],
                metadatas=[metadata]
            )
            print(f"Added CV: {cv_data['name']}")
        except Exception as e:
            print(f"Error adding CV: {e}")
    
    def search_with_weights(
        self, 
        query: str, 
        field: str = "Software Engineering",
        weights: Dict[str, float] = None,
        top_k: int = 10,
        filters: Dict = None,
        use_reranking: bool = True
    ) -> List[Dict]:
        """
        Advanced search with dynamic weighting
        
        Args:
            query: Search query
            field: Target field/industry
            weights: Dictionary of weights for each component
                     e.g., {'education': 0.25, 'experience': 0.35, 'skills': 0.30, ...}
            top_k: Number of results
            filters: Additional filters (years_of_experience, location, etc.)
            use_reranking: Whether to use cross-encoder re-ranking
        """
        
        # Default weights if not provided
        if weights is None:
            weights = {
                'education': 0.20,
                'experience': 0.30,
                'skills': 0.30,
                'projects': 0.10,
                'certifications': 0.10
            }
        
        # Normalize weights to sum to 1
        total_weight = sum(weights.values())
        normalized_weights = {k: v/total_weight for k, v in weights.items()}
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Retrieve more candidates for re-ranking
        n_retrieve = top_k * 3 if use_reranking and self.use_reranker else top_k
        
        # Search in vector database
        where_filter = {"field": field} if field else None
        
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_retrieve, self.collection.count()),
                where=where_filter
            )
        except Exception as e:
            print(f"Search error: {e}")
            return []
        
        # Process and score results
        candidates = []
        
        if results['metadatas'] and len(results['metadatas'][0]) > 0:
            for i, metadata in enumerate(results['metadatas'][0]):
                
                # Apply filters if provided
                if filters:
                    if not self._apply_filters(metadata, filters):
                        continue
                
                # Base semantic similarity
                distance = results['distances'][0][i]
                semantic_score = 1 / (1 + distance)
                
                # Calculate weighted score
                component_scores = self._calculate_component_scores(
                    query, 
                    metadata, 
                    results['documents'][0][i]
                )
                
                weighted_score = self._apply_weights(
                    component_scores,
                    normalized_weights,
                    semantic_score
                )
                
                # Create candidate dict
                candidate = {
                    'name': metadata['name'],
                    'email': metadata['email'],
                    'phone': metadata['phone'],
                    'location': metadata.get('location', 'Not specified'),
                    'linkedin': metadata.get('linkedin', 'Not provided'),
                    'github': metadata.get('github', 'Not provided'),
                    
                    'skills': json.loads(metadata['skills']),
                    'certifications': json.loads(metadata.get('certifications', '[]')),
                    'education': metadata['education'],
                    'experience': metadata['experience'],
                    'projects': metadata.get('projects', 'No projects listed'),
                    'achievements': metadata.get('achievements', 'No achievements listed'),
                    
                    'years_of_experience': float(metadata.get('years_of_experience', 0)),
                    'experience_level': metadata.get('experience_level', 'Unknown'),
                    'education_level': metadata.get('education_level', 'Not specified'),
                    
                    'summary': metadata['summary'],
                    'filename': metadata['filename'],
                    
                    # Scores
                    'semantic_score': semantic_score,
                    'weighted_score': weighted_score,
                    'final_score': weighted_score,  # Will be updated if re-ranked
                    'component_scores': component_scores,
                    
                    # Match explanation
                    'match_reason': self._generate_match_explanation(
                        query, metadata, component_scores, normalized_weights
                    )
                }
                
                candidates.append(candidate)
        
        # Re-rank if enabled
        if use_reranking and self.use_reranker and len(candidates) > 0:
            candidates = self._rerank_candidates(query, candidates)
        
        # Sort by final score and return top K
        candidates.sort(key=lambda x: x['final_score'], reverse=True)
        return candidates[:top_k]
    
    def _create_comprehensive_text(self, cv_data: Dict) -> str:
        """Create rich text representation for embedding"""
        
        parts = [
            f"Name: {cv_data['name']}",
            f"Field: {cv_data.get('field', 'Not specified')}",
            f"Skills: {', '.join(cv_data['skills'][:20])}",
            f"Certifications: {', '.join(cv_data.get('certifications', [])[:10])}",
            f"Education: {cv_data.get('education', 'Not specified')[:200]}",
            f"Experience: {cv_data.get('experience', 'Not specified')[:300]}",
            f"Projects: {cv_data.get('projects', 'No projects')[:200]}",
            f"Years of Experience: {cv_data.get('years_of_experience', 0)}",
            f"Level: {cv_data.get('experience_level', 'Unknown')}",
            f"Education Level: {cv_data.get('education_level', 'Not specified')}"
        ]
        
        return " | ".join(parts)
    
    def _calculate_component_scores(
        self, 
        query: str, 
        metadata: Dict,
        document: str
    ) -> Dict[str, float]:
        """Calculate individual scores for each CV component"""
        
        query_lower = query.lower()
        scores = {}
        
        # Skills score
        skills = json.loads(metadata['skills'])
        matching_skills = [s for s in skills if s.lower() in query_lower or 
                          any(word in s.lower() for word in query_lower.split())]
        scores['skills'] = min(len(matching_skills) / max(len(query_lower.split()), 1), 1.0)
        
        # Experience score (based on keywords and years)
        experience_text = metadata['experience'].lower()
        exp_keywords = [word for word in query_lower.split() if word in experience_text]
        scores['experience'] = min(len(exp_keywords) / max(len(query_lower.split()), 1), 1.0)
        
        # Education score
        education_text = metadata['education'].lower()
        edu_keywords = [word for word in query_lower.split() if word in education_text]
        scores['education'] = min(len(edu_keywords) / max(len(query_lower.split()), 1), 1.0)
        
        # Projects score
        projects_text = metadata.get('projects', '').lower()
        proj_keywords = [word for word in query_lower.split() if word in projects_text]
        scores['projects'] = min(len(proj_keywords) / max(len(query_lower.split()), 1), 1.0)
        
        # Certifications score
        certs = json.loads(metadata.get('certifications', '[]'))
        matching_certs = [c for c in certs if any(word in c.lower() for word in query_lower.split())]
        scores['certifications'] = min(len(matching_certs) / max(1, len(query_lower.split())), 1.0)
        
        return scores
    
    def _apply_weights(
        self,
        component_scores: Dict[str, float],
        weights: Dict[str, float],
        semantic_score: float
    ) -> float:
        """Apply dynamic weights to component scores"""
        
        # Weighted sum of component scores
        weighted_sum = 0.0
        for component, score in component_scores.items():
            weight = weights.get(component, 0.0)
            weighted_sum += score * weight
        
        # Combine with semantic similarity (70% weighted, 30% semantic)
        final_score = 0.7 * weighted_sum + 0.3 * semantic_score
        
        return final_score
    
    def _apply_filters(self, metadata: Dict, filters: Dict) -> bool:
        """Apply filters to candidate"""
        
        # Years of experience filter
        if 'min_experience' in filters:
            years = float(metadata.get('years_of_experience', 0))
            if years < filters['min_experience']:
                return False
        
        if 'max_experience' in filters:
            years = float(metadata.get('years_of_experience', 0))
            if years > filters['max_experience']:
                return False
        
        # Location filter
        if 'location' in filters:
            if filters['location'].lower() not in metadata.get('location', '').lower():
                return False
        
        # Education level filter
        if 'education_level' in filters:
            if filters['education_level'] != metadata.get('education_level', ''):
                return False
        
        return True
    
    def _rerank_candidates(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """Re-rank candidates using cross-encoder for better accuracy"""
        
        # Prepare query-document pairs
        pairs = [(query, cand['summary'][:500]) for cand in candidates]
        
        # Get re-ranking scores
        rerank_scores = self.reranker.predict(pairs)
        
        # Update final scores (combine weighted score with rerank score)
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(rerank_scores[i])
            # 60% weighted score, 40% rerank score
            candidate['final_score'] = 0.6 * candidate['weighted_score'] + 0.4 * candidate['rerank_score']
        
        return candidates
    
    def _generate_match_explanation(
        self,
        query: str,
        metadata: Dict,
        component_scores: Dict,
        weights: Dict
    ) -> str:
        """Generate human-readable explanation of why CV matches"""
        
        explanations = []
        
        # Top scoring components
        sorted_components = sorted(component_scores.items(), key=lambda x: x[1], reverse=True)
        
        for component, score in sorted_components[:3]:
            if score > 0.3:  # Only mention significant matches
                weight = weights.get(component, 0)
                if component == 'skills':
                    skills = json.loads(metadata['skills'])
                    matching = [s for s in skills if any(word in s.lower() for word in query.lower().split())]
                    if matching:
                        explanations.append(f"Strong {component} match: {', '.join(matching[:3])}")
                elif component == 'experience':
                    years = metadata.get('years_of_experience', 0)
                    explanations.append(f"{component.title()} matches ({years} years)")
                else:
                    explanations.append(f"{component.title()} relevant (score: {score:.0%})")
        
        # Experience level
        exp_level = metadata.get('experience_level', 'Unknown')
        if exp_level != 'Unknown':
            explanations.append(f"Experience level: {exp_level}")
        
        # Education
        edu_level = metadata.get('education_level', 'Not specified')
        if edu_level != 'Not specified':
            explanations.append(f"Education: {edu_level}")
        
        return " • ".join(explanations) if explanations else "Profile matches requirements"
    
    def get_all_cvs(self, field: Optional[str] = None) -> List[Dict]:
        """Get all CVs, optionally filtered by field"""
        
        try:
            where_filter = {"field": field} if field else None
            all_data = self.collection.get(where=where_filter)
            
            cvs = []
            if all_data['metadatas']:
                for metadata in all_data['metadatas']:
                    cv = {
                        'name': metadata['name'],
                        'field': metadata.get('field', 'Not specified'),
                        'email': metadata['email'],
                        'phone': metadata['phone'],
                        'location': metadata.get('location', 'Not specified'),
                        'skills': json.loads(metadata['skills']),
                        'certifications': json.loads(metadata.get('certifications', '[]')),
                        'education': metadata['education'],
                        'experience': metadata['experience'],
                        'years_of_experience': float(metadata.get('years_of_experience', 0)),
                        'experience_level': metadata.get('experience_level', 'Unknown'),
                        'education_level': metadata.get('education_level', 'Not specified'),
                        'summary': metadata['summary']
                    }
                    cvs.append(cv)
            
            return cvs
        except Exception as e:
            print(f"Error getting CVs: {e}")
            return []
    
    def clear_database(self):
        """Clear all CVs from database"""
        try:
            self.client.delete_collection("cvs_advanced")
            self.collection = self.client.create_collection("cvs_advanced")
            print("Database cleared!")
        except Exception as e:
            print(f"Error clearing database: {e}")
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        try:
            all_cvs = self.get_all_cvs()
            
            stats = {
                'total_cvs': len(all_cvs),
                'by_field': {},
                'by_experience_level': {},
                'by_education_level': {},
                'avg_experience_years': 0
            }
            
            # Count by field
            for cv in all_cvs:
                field = cv.get('field', 'Unknown')
                stats['by_field'][field] = stats['by_field'].get(field, 0) + 1
                
                exp_level = cv.get('experience_level', 'Unknown')
                stats['by_experience_level'][exp_level] = stats['by_experience_level'].get(exp_level, 0) + 1
                
                edu_level = cv.get('education_level', 'Not specified')
                stats['by_education_level'][edu_level] = stats['by_education_level'].get(edu_level, 0) + 1
            
            # Average experience
            if all_cvs:
                stats['avg_experience_years'] = sum(cv.get('years_of_experience', 0) for cv in all_cvs) / len(all_cvs)
            
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {'total_cvs': 0}
