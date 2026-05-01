import re
import os
from typing import Dict, List, Optional
from datetime import datetime
import PyPDF2
import docx
from utils.field_config import get_field_config

class AdvancedCVProcessor:
    """Advanced CV processor with detailed extraction capabilities"""
    
    def __init__(self, field="Software Engineering"):
        self.field = field
        self.field_config = get_field_config(field)
        self.skills_keywords = self.field_config["skills"]
        self.certifications_keywords = self.field_config.get("certifications", [])
    
    def process(self, file_path: str, filename: str, field: str = None) -> Dict:
        """Process a CV file and extract comprehensive information"""
        
        if field:
            self.field = field
            self.field_config = get_field_config(field)
            self.skills_keywords = self.field_config["skills"]
            self.certifications_keywords = self.field_config.get("certifications", [])
        
        # Extract text
        text = self._read_file(file_path)
        
        # Extract comprehensive information
        cv_data = {
            'filename': filename,
            'field': self.field,
            'name': self._extract_name(text, filename),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'location': self._extract_location(text),
            'linkedin': self._extract_linkedin(text),
            'github': self._extract_github(text),
            'website': self._extract_website(text),
            
            # Core sections
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience': self._extract_experience(text),
            'projects': self._extract_projects(text),
            'certifications': self._extract_certifications(text),
            'licenses': self._extract_licenses(text),
            'achievements': self._extract_achievements(text),
            'languages': self._extract_languages(text),
            
            # Calculated fields
            'years_of_experience': self._calculate_experience_years(text),
            'experience_level': self._determine_experience_level(text),
            'education_level': self._determine_education_level(text),
            
            # Summary
            'summary': self._create_summary(text),
            'full_text': text,
            
            # Metadata
            'processed_date': datetime.now().isoformat(),
            'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
        }
        
        return cv_data
    
    def _read_file(self, path: str) -> str:
        """Read file content based on format"""
        
        if path.endswith('.pdf'):
            return self._read_pdf(path)
        elif path.endswith('.docx'):
            return self._read_docx(path)
        elif path.endswith('.txt'):
            return self._read_txt(path)
        return ""
    
    def _read_pdf(self, path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def _read_docx(self, path: str) -> str:
        """Extract text from DOCX"""
        text = ""
        try:
            doc = docx.Document(path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text
    
    def _read_txt(self, path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    
    def _extract_name(self, text: str, filename: str) -> str:
        """Extract candidate name"""
        lines = text.split('\n')
        for line in lines[:7]:
            line = line.strip()
            # Name heuristics
            if line and 2 <= len(line.split()) <= 4 and len(line) < 50:
                # Check if it looks like a name (no numbers, not all caps unless 2 words)
                if not re.search(r'\d', line):
                    words = line.split()
                    if len(words) >= 2:
                        return line
        
        return filename.replace('.pdf', '').replace('.docx', '').replace('.txt', '').replace('_', ' ').title()
    
    def _extract_email(self, text: str) -> str:
        """Extract email address"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return emails[0] if emails else "Not provided"
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number"""
        patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}-\d{3}-\d{4}',
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{10}'
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        
        return "Not provided"
    
    def _extract_location(self, text: str) -> str:
        """Extract location/address"""
        # Look for city, state patterns
        location_pattern = r'([A-Z][a-z]+,\s*[A-Z]{2}|\b(?:New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose|Austin|Jacksonville|Fort Worth|Columbus|Charlotte|San Francisco|Indianapolis|Seattle|Denver|Washington|Boston|Nashville|Baltimore|Oklahoma City|Portland|Las Vegas|Milwaukee|Albuquerque|Tucson|Fresno|Sacramento|Kansas City|Atlanta|Miami|Raleigh|Omaha|Colorado Springs|Virginia Beach)\b)'
        locations = re.findall(location_pattern, text, re.IGNORECASE)
        return locations[0] if locations else "Not specified"
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL"""
        pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(pattern, text.lower())
        return f"https://{linkedin[0]}" if linkedin else "Not provided"
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub URL"""
        pattern = r'github\.com/[\w-]+'
        github = re.findall(pattern, text.lower())
        return f"https://{github[0]}" if github else "Not provided"
    
    def _extract_website(self, text: str) -> str:
        """Extract personal website"""
        pattern = r'https?://(?:www\.)?[\w\-\.]+\.\w{2,}(?:/[\w\-\.]*)*'
        websites = re.findall(pattern, text)
        # Filter out common sites (LinkedIn, GitHub, email providers)
        excluded = ['linkedin', 'github', 'gmail', 'yahoo', 'outlook', 'hotmail']
        for site in websites:
            if not any(ex in site.lower() for ex in excluded):
                return site
        return "Not provided"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills based on field"""
        text_lower = text.lower()
        found_skills = set()
        
        # Match against field-specific skills
        for skill in self.skills_keywords:
            if skill.lower() in text_lower:
                found_skills.add(skill.title())
        
        # Also check skills section specifically
        skills_section = re.search(
            r'(?:technical\s+)?skills?:?(.*?)(?:experience|education|projects|certifications|$)',
            text_lower, 
            re.DOTALL | re.IGNORECASE
        )
        
        if skills_section:
            skills_text = skills_section.group(1)
            # Extract comma-separated or newline-separated skills
            potential_skills = re.split(r'[,\n•·]', skills_text)
            for skill in potential_skills:
                skill = skill.strip()
                if 2 < len(skill) < 30 and not skill.isdigit():
                    found_skills.add(skill.title())
        
        return sorted(list(found_skills))[:30]  # Return top 30 skills
    
    def _extract_education(self, text: str) -> str:
        """Extract education information"""
        keywords = ['education', 'degree', 'bachelor', 'master', 'phd', 'doctorate', 'university', 'college', 'b.s.', 'm.s.', 'b.a.', 'm.a.']
        
        lines = text.split('\n')
        education_lines = []
        capture = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Start capturing
            if any(keyword in line_lower for keyword in keywords):
                capture = True
            
            # Capture lines
            if capture:
                if line.strip():
                    education_lines.append(line.strip())
                
                # Stop at next major section
                if i > 0 and any(keyword in line_lower for keyword in ['experience', 'work history', 'employment', 'skills', 'projects']):
                    if len(education_lines) > 2:
                        break
            
            if len(education_lines) > 10:
                break
        
        return ' '.join(education_lines[:10]) if education_lines else "Not specified"
    
    def _extract_experience(self, text: str) -> str:
        """Extract work experience"""
        keywords = ['experience', 'work history', 'employment', 'professional experience', 'work experience']
        
        lines = text.split('\n')
        experience_lines = []
        capture = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in keywords):
                capture = True
            
            if capture:
                if line.strip():
                    experience_lines.append(line.strip())
                
                # Stop at next section
                if i > 0 and any(keyword in line_lower for keyword in ['education', 'skills', 'projects', 'certifications', 'licenses']):
                    if len(experience_lines) > 3:
                        break
            
            if len(experience_lines) > 20:
                break
        
        return ' '.join(experience_lines[:20]) if experience_lines else "Not specified"
    
    def _extract_projects(self, text: str) -> str:
        """Extract projects"""
        keywords = ['projects', 'portfolio', 'work samples']
        
        lines = text.split('\n')
        project_lines = []
        capture = False
        
        for line in lines:
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in keywords):
                capture = True
            
            if capture:
                if line.strip():
                    project_lines.append(line.strip())
                
                if any(keyword in line_lower for keyword in ['education', 'skills', 'experience', 'certifications']):
                    if len(project_lines) > 2:
                        break
            
            if len(project_lines) > 15:
                break
        
        return ' '.join(project_lines[:15]) if project_lines else "No projects listed"
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        text_lower = text.lower()
        found_certs = set()
        
        # Match field-specific certifications
        for cert in self.certifications_keywords:
            if cert.lower() in text_lower:
                found_certs.add(cert.title())
        
        # Also look for certification section
        cert_section = re.search(
            r'certifications?:?(.*?)(?:education|experience|skills|$)',
            text_lower,
            re.DOTALL | re.IGNORECASE
        )
        
        if cert_section:
            cert_text = cert_section.group(1)
            potential_certs = re.split(r'[,\n•·]', cert_text)
            for cert in potential_certs:
                cert = cert.strip()
                if 3 < len(cert) < 50:
                    found_certs.add(cert.title())
        
        return sorted(list(found_certs))
    
    def _extract_licenses(self, text: str) -> List[str]:
        """Extract professional licenses"""
        license_keywords = ['license', 'licensed', 'registration', 'registered']
        text_lower = text.lower()
        found_licenses = []
        
        # Look for license section
        for keyword in license_keywords:
            if keyword in text_lower:
                # Extract context around keyword
                pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
                matches = re.findall(pattern, text_lower)
                found_licenses.extend([m.strip() for m in matches])
        
        return list(set(found_licenses))[:5]
    
    def _extract_achievements(self, text: str) -> str:
        """Extract achievements and awards"""
        keywords = ['achievements', 'awards', 'honors', 'recognition', 'accomplishments']
        
        lines = text.split('\n')
        achievement_lines = []
        capture = False
        
        for line in lines:
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in keywords):
                capture = True
            
            if capture:
                if line.strip():
                    achievement_lines.append(line.strip())
                
                if any(keyword in line_lower for keyword in ['education', 'skills', 'experience']):
                    if len(achievement_lines) > 2:
                        break
            
            if len(achievement_lines) > 10:
                break
        
        return ' '.join(achievement_lines[:10]) if achievement_lines else "No achievements listed"
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract spoken languages"""
        language_keywords = ['english', 'spanish', 'french', 'german', 'chinese', 'japanese', 
                             'arabic', 'hindi', 'urdu', 'russian', 'portuguese', 'italian']
        text_lower = text.lower()
        found_languages = []
        
        for lang in language_keywords:
            if lang in text_lower:
                found_languages.append(lang.title())
        
        return found_languages
    
    def _calculate_experience_years(self, text: str) -> float:
        """Calculate total years of experience"""
        # Look for patterns like "5 years", "5+ years", "2-4 years"
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience:?\s*(\d+)\+?\s*years?'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(y) for y in matches])
        
        # Also try to extract from date ranges (2020-2024 = 4 years)
        date_ranges = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', text.lower())
        for start, end in date_ranges:
            end_year = datetime.now().year if end in ['present', 'current'] else int(end)
            years.append(end_year - int(start))
        
        return max(years) if years else 0.0
    
    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level based on years"""
        years = self._calculate_experience_years(text)
        levels = self.field_config.get("experience_levels", {})
        
        for level, range_dict in levels.items():
            if range_dict["min_years"] <= years <= range_dict["max_years"]:
                return level.title()
        
        return "Unknown"
    
    def _determine_education_level(self, text: str) -> str:
        """Determine highest education level"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['phd', 'ph.d', 'doctorate', 'doctoral']):
            return "PhD"
        elif any(keyword in text_lower for keyword in ['master', 'm.s.', 'm.a.', 'mba', 'msc']):
            return "Master's"
        elif any(keyword in text_lower for keyword in ['bachelor', 'b.s.', 'b.a.', 'b.tech', 'bsc']):
            return "Bachelor's"
        elif any(keyword in text_lower for keyword in ['associate', 'diploma']):
            return "Associate/Diploma"
        else:
            return "Not specified"
    
    def _create_summary(self, text: str) -> str:
        """Create executive summary"""
        # Take first 600 characters
        summary = text[:600].replace('\n', ' ').strip()
        if len(text) > 600:
            summary += "..."
        return summary
