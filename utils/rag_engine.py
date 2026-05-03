import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict, Optional
import json
import os
import numpy as np
from datetime import datetime


class AdvancedRAGEngine:
    """
    Advanced RAG engine with session-based data isolation.
    Each session_id sees ONLY its own CVs — no data leakage between users.
    """

    def __init__(
        self,
        model_name: str = "all-mpnet-base-v2",
        use_reranker: bool = True,
        session_id: str = "default",
    ):
        self.session_id = session_id

        print(f"Loading embedding model: {model_name}...")
        self.embedding_model = SentenceTransformer(model_name)

        self.use_reranker = use_reranker
        self.reranker = None
        if use_reranker:
            try:
                print("Loading re-ranker model...")
                self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
            except Exception as e:
                print(f"Warning: re-ranker unavailable ({e}). Disabling.")
                self.use_reranker = False

        # ChromaDB setup — single shared collection, filtered by session_id
        os.makedirs("./data/chroma_db", exist_ok=True)
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        try:
            self.collection = self.client.get_collection("cvs_advanced")
        except Exception:
            self.collection = self.client.create_collection(
                "cvs_advanced",
                metadata={"hnsw:space": "cosine"},
            )

        print(f"RAG Engine ready (session: {self.session_id})")

    # ------------------------------------------------------------------ #
    #  SESSION MANAGEMENT                                                  #
    # ------------------------------------------------------------------ #

    def set_session(self, session_id: str):
        """Switch active session (call when Streamlit session_id changes)."""
        self.session_id = session_id

    def _session_filter(self, extra: Optional[Dict] = None) -> Dict:
        """Build a ChromaDB where-filter scoped to this session."""
        base = {"session_id": {"$eq": self.session_id}}
        if extra:
            return {"$and": [base, extra]}
        return base

    # ------------------------------------------------------------------ #
    #  PUBLIC API                                                          #
    # ------------------------------------------------------------------ #

    def add_cv(self, cv_data: Dict, field: str = "Software Engineering"):
        """Add CV tagged with the current session_id."""
        cv_text = self._create_comprehensive_text(cv_data)
        embedding = self.embedding_model.encode(cv_text).tolist()

        # Unique ID scoped to session so same filename from two users never collide
        doc_id = f"{self.session_id}__{cv_data['filename']}"

        metadata = {
            "session_id":         self.session_id,
            "name":               cv_data.get("name", "Unknown"),
            "field":              field,
            "email":              cv_data.get("email", "Not provided"),
            "phone":              cv_data.get("phone", "Not provided"),
            "location":           cv_data.get("location", "Not specified"),
            "linkedin":           cv_data.get("linkedin", "Not provided"),
            "github":             cv_data.get("github", "Not provided"),
            "skills":             json.dumps(cv_data.get("skills", [])),
            "certifications":     json.dumps(cv_data.get("certifications", [])),
            "licenses":           json.dumps(cv_data.get("licenses", [])),
            "languages":          json.dumps(cv_data.get("languages", [])),
            "education":          str(cv_data.get("education", "Not specified"))[:500],
            "experience":         str(cv_data.get("experience", "Not specified"))[:500],
            "projects":           str(cv_data.get("projects", "No projects listed"))[:500],
            "achievements":       str(cv_data.get("achievements", "No achievements listed"))[:300],
            "summary":            str(cv_data.get("summary", ""))[:500],
            "years_of_experience": str(cv_data.get("years_of_experience", 0)),
            "experience_level":   cv_data.get("experience_level", "Unknown"),
            "education_level":    cv_data.get("education_level", "Not specified"),
            "filename":           cv_data["filename"],
            "processed_date":     cv_data.get("processed_date", datetime.now().isoformat()),
        }

        try:
            self.collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[cv_text],
                metadatas=[metadata],
            )
        except Exception as e:
            print(f"Error adding CV: {e}")

    def search_with_weights(
        self,
        query: str,
        field: str = "Software Engineering",
        weights: Optional[Dict[str, float]] = None,
        top_k: int = 10,
        filters: Optional[Dict] = None,
        use_reranking: bool = True,
    ) -> List[Dict]:
        """Semantic search scoped to current session."""

        total = self._safe_count()
        if total == 0:
            return []

        # Default weights
        if weights is None:
            weights = {"education": 0.20, "experience": 0.30, "skills": 0.30,
                       "projects": 0.10, "certifications": 0.10}

        total_w = sum(weights.values()) or 1.0
        norm_weights = {k: v / total_w for k, v in weights.items()}

        query_embedding = self.embedding_model.encode(query).tolist()

        n_retrieve = (top_k * 3) if (use_reranking and self.use_reranker) else top_k
        n_retrieve = max(1, min(n_retrieve, total))

        # Session-scoped + optional field filter
        field_extra = {"field": {"$eq": field}} if field else None
        where = self._session_filter(field_extra)

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_retrieve,
                where=where,
                include=["metadatas", "documents", "distances"],
            )
        except Exception as e:
            print(f"Search error: {e}")
            return []

        candidates = []
        if results.get("metadatas") and results["metadatas"][0]:
            for i, metadata in enumerate(results["metadatas"][0]):
                if filters and not self._apply_filters(metadata, filters):
                    continue

                # Cosine distance ∈ [0,2] → similarity ∈ [0,1]
                distance = results["distances"][0][i]
                semantic_score = max(0.0, 1.0 - distance / 2.0)

                comp_scores = self._calculate_component_scores(
                    query, metadata, results["documents"][0][i]
                )
                weighted_score = self._apply_weights(comp_scores, norm_weights, semantic_score)

                candidate = {
                    "name":                metadata.get("name", "Unknown"),
                    "email":               metadata.get("email", "Not provided"),
                    "phone":               metadata.get("phone", "Not provided"),
                    "location":            metadata.get("location", "Not specified"),
                    "linkedin":            metadata.get("linkedin", "Not provided"),
                    "github":              metadata.get("github", "Not provided"),
                    "skills":              self._safe_json(metadata.get("skills", "[]")),
                    "certifications":      self._safe_json(metadata.get("certifications", "[]")),
                    "education":           metadata.get("education", "Not specified"),
                    "experience":          metadata.get("experience", "Not specified"),
                    "projects":            metadata.get("projects", ""),
                    "achievements":        metadata.get("achievements", ""),
                    "years_of_experience": float(metadata.get("years_of_experience", 0)),
                    "experience_level":    metadata.get("experience_level", "Unknown"),
                    "education_level":     metadata.get("education_level", "Not specified"),
                    "summary":             metadata.get("summary", ""),
                    "filename":            metadata.get("filename", ""),
                    "semantic_score":      round(semantic_score, 4),
                    "weighted_score":      round(weighted_score, 4),
                    "final_score":         round(weighted_score, 4),
                    "component_scores":    comp_scores,
                    "match_reason":        self._explain(query, metadata, comp_scores, norm_weights),
                }
                candidates.append(candidate)

        if use_reranking and self.use_reranker and self.reranker and candidates:
            candidates = self._rerank(query, candidates)

        candidates.sort(key=lambda x: x["final_score"], reverse=True)
        return candidates[:top_k]

    def get_all_cvs(self, field: Optional[str] = None) -> List[Dict]:
        """Get all CVs for the current session only."""
        try:
            field_extra = {"field": {"$eq": field}} if field else None
            where = self._session_filter(field_extra)
            data = self.collection.get(where=where)

            cvs = []
            for meta in (data.get("metadatas") or []):
                cvs.append({
                    "name":                meta.get("name", "Unknown"),
                    "field":               meta.get("field", "Not specified"),
                    "email":               meta.get("email", "Not provided"),
                    "phone":               meta.get("phone", "Not provided"),
                    "location":            meta.get("location", "Not specified"),
                    "skills":              self._safe_json(meta.get("skills", "[]")),
                    "certifications":      self._safe_json(meta.get("certifications", "[]")),
                    "education":           meta.get("education", "Not specified"),
                    "experience":          meta.get("experience", "Not specified"),
                    "years_of_experience": float(meta.get("years_of_experience", 0)),
                    "experience_level":    meta.get("experience_level", "Unknown"),
                    "education_level":     meta.get("education_level", "Not specified"),
                    "summary":             meta.get("summary", ""),
                    "filename":            meta.get("filename", ""),
                })
            return cvs
        except Exception as e:
            print(f"Error getting CVs: {e}")
            return []

    def clear_session_cvs(self):
        """Delete ALL CVs belonging to the current session only."""
        try:
            where = self._session_filter()
            data = self.collection.get(where=where, include=[])
            ids = data.get("ids", [])
            if ids:
                self.collection.delete(ids=ids)
            print(f"Cleared {len(ids)} CVs for session {self.session_id}")
        except Exception as e:
            print(f"Error clearing session CVs: {e}")

    # Keep old name for backward compat (clears current session only)
    def clear_database(self):
        self.clear_session_cvs()

    def get_statistics(self) -> Dict:
        """Stats for current session only."""
        try:
            all_cvs = self.get_all_cvs()
            stats: Dict = {
                "total_cvs": len(all_cvs),
                "by_field": {},
                "by_experience_level": {},
                "by_education_level": {},
                "avg_experience_years": 0.0,
            }
            for cv in all_cvs:
                f  = cv.get("field", "Unknown")
                el = cv.get("experience_level", "Unknown")
                ed = cv.get("education_level", "Not specified")
                stats["by_field"][f]  = stats["by_field"].get(f, 0) + 1
                stats["by_experience_level"][el] = stats["by_experience_level"].get(el, 0) + 1
                stats["by_education_level"][ed]  = stats["by_education_level"].get(ed, 0) + 1

            if all_cvs:
                stats["avg_experience_years"] = (
                    sum(cv.get("years_of_experience", 0) for cv in all_cvs) / len(all_cvs)
                )
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"total_cvs": 0}

    # ------------------------------------------------------------------ #
    #  PRIVATE HELPERS                                                     #
    # ------------------------------------------------------------------ #

    def _safe_count(self) -> int:
        """Count only this session's documents."""
        try:
            data = self.collection.get(where=self._session_filter(), include=[])
            return len(data.get("ids", []))
        except Exception:
            return 0

    @staticmethod
    def _safe_json(value: str) -> list:
        try:
            r = json.loads(value)
            return r if isinstance(r, list) else []
        except Exception:
            return []

    def _create_comprehensive_text(self, cv: Dict) -> str:
        return " | ".join([
            f"Name: {cv.get('name', '')}",
            f"Field: {cv.get('field', '')}",
            f"Skills: {', '.join(cv.get('skills', [])[:20])}",
            f"Certifications: {', '.join(cv.get('certifications', [])[:10])}",
            f"Education: {str(cv.get('education', ''))[:200]}",
            f"Experience: {str(cv.get('experience', ''))[:300]}",
            f"Projects: {str(cv.get('projects', ''))[:200]}",
            f"Years of Experience: {cv.get('years_of_experience', 0)}",
            f"Level: {cv.get('experience_level', '')}",
            f"Education Level: {cv.get('education_level', '')}",
        ])

    def _calculate_component_scores(self, query: str, meta: Dict, doc: str) -> Dict[str, float]:
        import re as _re
        query_words = set(query.lower().split())
        n = max(len(query_words), 1)
        scores = {}

        # Skills
        skills = self._safe_json(meta.get("skills", "[]"))
        matched = [s for s in skills if any(qw in s.lower() for qw in query_words)]
        scores["skills"] = min(len(matched) / n, 1.0)

        # Experience
        exp_text = meta.get("experience", "").lower()
        scores["experience"] = min(sum(1 for w in query_words if w in exp_text) / n, 1.0)
        # Bonus for years match
        try:
            years = float(meta.get("years_of_experience", 0))
            m = _re.search(r"(\d+)\+?\s*years?", query.lower())
            if m and years >= int(m.group(1)):
                scores["experience"] = min(scores["experience"] + 0.2, 1.0)
        except Exception:
            pass

        # Education
        edu_text = meta.get("education", "").lower()
        scores["education"] = min(sum(1 for w in query_words if w in edu_text) / n, 1.0)

        # Projects
        proj_text = meta.get("projects", "").lower()
        scores["projects"] = min(sum(1 for w in query_words if w in proj_text) / n, 1.0)

        # Certifications
        certs = self._safe_json(meta.get("certifications", "[]"))
        matched_c = [c for c in certs if any(qw in c.lower() for qw in query_words)]
        scores["certifications"] = min(len(matched_c) / n, 1.0)

        return scores

    def _apply_weights(self, comp: Dict, weights: Dict, semantic: float) -> float:
        ws = sum(comp.get(k, 0.0) * weights.get(k, 0.0) for k in weights)
        return min(max(0.70 * ws + 0.30 * semantic, 0.0), 1.0)

    def _apply_filters(self, meta: Dict, filters: Dict) -> bool:
        years = float(meta.get("years_of_experience", 0))
        if "min_experience" in filters and years < filters["min_experience"]:
            return False
        if "max_experience" in filters and years > filters["max_experience"]:
            return False
        if "location" in filters:
            if filters["location"].lower() not in meta.get("location", "").lower():
                return False
        if "education_level" in filters:
            if filters["education_level"] != meta.get("education_level", ""):
                return False
        return True

    def _rerank(self, query: str, candidates: List[Dict]) -> List[Dict]:
        pairs = [(query, c.get("summary", "")[:500]) for c in candidates]
        try:
            raw = self.reranker.predict(pairs)
        except Exception as e:
            print(f"Reranker error: {e}")
            return candidates

        # Sigmoid → [0, 1]
        norm = 1.0 / (1.0 + np.exp(-np.array(raw, dtype=float)))
        for i, c in enumerate(candidates):
            c["rerank_score"] = round(float(norm[i]), 4)
            c["final_score"]  = round(min(0.60 * c["weighted_score"] + 0.40 * c["rerank_score"], 1.0), 4)
        return candidates

    def _explain(self, query: str, meta: Dict, comp: Dict, weights: Dict) -> str:
        parts = []
        for key, score in sorted(comp.items(), key=lambda x: x[1], reverse=True)[:3]:
            if score < 0.05:
                continue
            if key == "skills":
                skills = self._safe_json(meta.get("skills", "[]"))
                matched = [s for s in skills if any(w in s.lower() for w in query.lower().split())]
                if matched:
                    parts.append(f"Skills matched: {', '.join(matched[:4])}")
            elif key == "experience":
                parts.append(f"Experience: {meta.get('years_of_experience', 0)} yrs")
            elif key == "certifications":
                certs = self._safe_json(meta.get("certifications", "[]"))
                if certs:
                    parts.append(f"Certs: {', '.join(certs[:2])}")
            else:
                parts.append(f"{key.title()} ({score:.0%})")

        el = meta.get("experience_level", "")
        if el and el != "Unknown":
            parts.append(f"Level: {el}")
        ed = meta.get("education_level", "")
        if ed and ed != "Not specified":
            parts.append(f"Edu: {ed}")

        return " • ".join(parts) if parts else "Profile matches requirements"
