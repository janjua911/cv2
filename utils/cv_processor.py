import re
import os
from typing import Dict, List, Optional
from datetime import datetime

import PyPDF2
import docx

from utils.field_config import get_field_config


class AdvancedCVProcessor:
    """Advanced CV processor with detailed extraction capabilities"""

    def __init__(self, field: str = "Software Engineering"):
        self.field = field
        self.field_config = get_field_config(field)
        self.skills_keywords: List[str] = self.field_config.get("skills", [])
        self.certifications_keywords: List[str] = self.field_config.get("certifications", [])

    # ------------------------------------------------------------------ #
    #  PUBLIC API                                                          #
    # ------------------------------------------------------------------ #

    def process(self, file_path: str, filename: str, field: str = None) -> Dict:
        """Process a CV file and extract comprehensive information"""

        if field and field != self.field:
            self.field = field
            self.field_config = get_field_config(field)
            self.skills_keywords = self.field_config.get("skills", [])
            self.certifications_keywords = self.field_config.get("certifications", [])

        text = self._read_file(file_path)

        cv_data = {
            "filename": filename,
            "field": self.field,
            "name": self._extract_name(text, filename),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "location": self._extract_location(text),
            "linkedin": self._extract_linkedin(text),
            "github": self._extract_github(text),
            "website": self._extract_website(text),
            # Core sections
            "skills": self._extract_skills(text),
            "education": self._extract_education(text),
            "experience": self._extract_experience(text),
            "projects": self._extract_projects(text),
            "certifications": self._extract_certifications(text),
            "licenses": self._extract_licenses(text),
            "achievements": self._extract_achievements(text),
            "languages": self._extract_languages(text),
            # Calculated fields
            "years_of_experience": self._calculate_experience_years(text),
            "experience_level": self._determine_experience_level(text),
            "education_level": self._determine_education_level(text),
            # Summary
            "summary": self._create_summary(text),
            "full_text": text,
            # Metadata
            "processed_date": datetime.now().isoformat(),
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
        }

        return cv_data

    # ------------------------------------------------------------------ #
    #  FILE READING                                                        #
    # ------------------------------------------------------------------ #

    def _read_file(self, path: str) -> str:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            return self._read_pdf(path)
        elif ext == ".docx":
            return self._read_docx(path)
        elif ext == ".txt":
            return self._read_txt(path)
        return ""

    def _read_pdf(self, path: str) -> str:
        text = ""
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"Error reading PDF {path}: {e}")
        return text

    def _read_docx(self, path: str) -> str:
        text = ""
        try:
            doc = docx.Document(path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {path}: {e}")
        return text

    def _read_txt(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT {path}: {e}")
            return ""

    # ------------------------------------------------------------------ #
    #  PERSONAL INFO EXTRACTION                                            #
    # ------------------------------------------------------------------ #

    def _extract_name(self, text: str, filename: str) -> str:
        """Extract candidate name from the first few lines"""
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]

        # Section headers and noise to skip
        skip_patterns = re.compile(
            r"(curriculum vitae|resume|cv|objective|summary|profile|contact|"
            r"address|phone|email|linkedin|github|www\.|http)",
            re.IGNORECASE,
        )

        for line in lines[:10]:
            # Must have 2-4 words, all alphabetic (allow hyphens & apostrophes)
            words = line.split()
            if 2 <= len(words) <= 4:
                if all(re.match(r"^[A-Za-z\-'\.]+$", w) for w in words):
                    if not skip_patterns.search(line):
                        return line.title()

        # Fallback: derive from filename
        base = os.path.splitext(filename)[0]
        return base.replace("_", " ").replace("-", " ").title()

    def _extract_email(self, text: str) -> str:
        pattern = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
        matches = re.findall(pattern, text)
        return matches[0] if matches else "Not provided"

    def _extract_phone(self, text: str) -> str:
        patterns = [
            r"\+?1?\s*[\-.]?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}",
            r"\+\d{1,3}[\s\-]?\d{6,12}",
            r"\d{10}",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        return "Not provided"

    def _extract_location(self, text: str) -> str:
        # City, STATE pattern (e.g. Austin, TX)
        pattern = r"\b[A-Z][a-zA-Z\s]+,\s*[A-Z]{2}\b"
        matches = re.findall(pattern, text)
        if matches:
            return matches[0].strip()

        # Known major cities
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "San Francisco", "Seattle", "Boston", "Austin", "Denver",
            "Atlanta", "Miami", "Dallas", "San Diego", "Washington",
            "Islamabad", "Karachi", "Lahore", "London", "Toronto", "Sydney",
        ]
        text_lower = text.lower()
        for city in cities:
            if city.lower() in text_lower:
                return city

        return "Not specified"

    def _extract_linkedin(self, text: str) -> str:
        match = re.search(r"linkedin\.com/in/[\w\-]+", text, re.IGNORECASE)
        return f"https://{match.group()}" if match else "Not provided"

    def _extract_github(self, text: str) -> str:
        match = re.search(r"github\.com/[\w\-]+", text, re.IGNORECASE)
        return f"https://{match.group()}" if match else "Not provided"

    def _extract_website(self, text: str) -> str:
        pattern = r"https?://(?:www\.)?[\w\-\.]+\.\w{2,}(?:/[\w\-\./?=%&]*)*"
        excluded = {"linkedin", "github", "gmail", "yahoo", "outlook", "hotmail"}
        for url in re.findall(pattern, text):
            if not any(ex in url.lower() for ex in excluded):
                return url
        return "Not provided"

    # ------------------------------------------------------------------ #
    #  CONTENT EXTRACTION                                                  #
    # ------------------------------------------------------------------ #

    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills based on field keywords"""
        text_lower = text.lower()
        found_skills: set = set()

        # 1) Match against field-specific keyword list
        for skill in self.skills_keywords:
            # Use word-boundary-aware matching for short tokens
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text_lower):
                found_skills.add(skill.title())

        # 2) Extract from an explicit "Skills" section (comma/bullet separated)
        skills_section_match = re.search(
            r"(?:technical\s+)?skills?\s*[:\-]\s*(.*?)(?=\n\s*\n|\Z|"
            r"(?:experience|education|projects?|certifications?|work\s+history))",
            text_lower,
            re.DOTALL | re.IGNORECASE,
        )
        if skills_section_match:
            raw = skills_section_match.group(1)
            for token in re.split(r"[,\n•·|/]", raw):
                token = token.strip().strip("•·-–—").strip()
                if 2 < len(token) < 35 and not token.isdigit():
                    found_skills.add(token.title())

        return sorted(found_skills)[:30]

    def _extract_section(
        self,
        text: str,
        start_keywords: List[str],
        stop_keywords: List[str],
        max_lines: int = 20,
    ) -> str:
        """Generic section extractor"""
        lines = text.split("\n")
        section_lines: List[str] = []
        capturing = False

        for line in lines:
            line_lower = line.lower().strip()

            if not capturing:
                if any(kw in line_lower for kw in start_keywords):
                    capturing = True
                    section_lines.append(line.strip())
            else:
                # Stop when we hit a different major section
                if any(kw in line_lower for kw in stop_keywords) and section_lines:
                    break
                if line.strip():
                    section_lines.append(line.strip())
                if len(section_lines) >= max_lines:
                    break

        return " ".join(section_lines).strip() if section_lines else "Not specified"

    def _extract_education(self, text: str) -> str:
        return self._extract_section(
            text,
            start_keywords=["education", "academic", "qualification", "degree"],
            stop_keywords=["experience", "work history", "employment", "skills", "projects"],
            max_lines=10,
        )

    def _extract_experience(self, text: str) -> str:
        return self._extract_section(
            text,
            start_keywords=[
                "experience", "work history", "employment",
                "professional experience", "work experience",
            ],
            stop_keywords=["education", "skills", "projects", "certifications", "licenses"],
            max_lines=25,
        )

    def _extract_projects(self, text: str) -> str:
        result = self._extract_section(
            text,
            start_keywords=["projects", "portfolio", "work samples"],
            stop_keywords=["education", "skills", "experience", "certifications"],
            max_lines=15,
        )
        return result if result != "Not specified" else "No projects listed"

    def _extract_certifications(self, text: str) -> List[str]:
        text_lower = text.lower()
        found: set = set()

        for cert in self.certifications_keywords:
            if re.search(r"\b" + re.escape(cert.lower()) + r"\b", text_lower):
                found.add(cert.upper())

        # Also parse a Certifications section
        match = re.search(
            r"certifications?\s*[:\-]?\s*(.*?)(?=\n\s*\n|\Z|"
            r"(?:education|experience|skills|work\s+history))",
            text_lower,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            for token in re.split(r"[,\n•·]", match.group(1)):
                token = token.strip()
                if 3 < len(token) < 60:
                    found.add(token.title())

        return sorted(found)

    def _extract_licenses(self, text: str) -> List[str]:
        found: set = set()
        pattern = r".{0,60}(?:licens(?:e|ed|ing)|registered|registration).{0,60}"
        for match in re.finditer(pattern, text, re.IGNORECASE):
            snippet = match.group().strip()
            if len(snippet) > 5:
                found.add(snippet)
        return list(found)[:5]

    def _extract_achievements(self, text: str) -> str:
        result = self._extract_section(
            text,
            start_keywords=["achievement", "award", "honor", "recognition", "accomplishment"],
            stop_keywords=["education", "skills", "experience"],
            max_lines=10,
        )
        return result if result != "Not specified" else "No achievements listed"

    def _extract_languages(self, text: str) -> List[str]:
        known = [
            "english", "spanish", "french", "german", "chinese", "japanese",
            "arabic", "hindi", "urdu", "russian", "portuguese", "italian",
            "korean", "dutch", "swedish", "turkish",
        ]
        text_lower = text.lower()
        return [lang.title() for lang in known if re.search(r"\b" + lang + r"\b", text_lower)]

    # ------------------------------------------------------------------ #
    #  CALCULATED FIELDS                                                   #
    # ------------------------------------------------------------------ #

    def _calculate_experience_years(self, text: str) -> float:
        """
        Estimate total years of experience.
        Strategy:
          1. Look for explicit "N years experience" statements → take max.
          2. Sum non-overlapping date ranges (YYYY–YYYY or YYYY–present).
          Return the greater of the two.
        """
        years_list: List[float] = []

        # --- Pattern 1: "5 years of experience" / "5+ years" ---
        for m in re.finditer(
            r"(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience",
            text,
            re.IGNORECASE,
        ):
            years_list.append(float(m.group(1)))

        # --- Pattern 2: date ranges ---
        current_year = datetime.now().year
        date_range_years: List[int] = []
        for m in re.finditer(
            r"(\d{4})\s*[-–—]\s*((\d{4})|present|current|now)",
            text,
            re.IGNORECASE,
        ):
            start = int(m.group(1))
            end_raw = m.group(2).lower()
            end = current_year if end_raw in ("present", "current", "now") else int(end_raw)
            duration = end - start
            if 0 < duration <= 50:          # Sanity check
                date_range_years.append(duration)

        if date_range_years:
            years_list.append(float(sum(date_range_years)))

        if not years_list:
            return 0.0

        # Return the maximum credible value
        return min(max(years_list), 50.0)

    def _determine_experience_level(self, text: str) -> str:
        """
        Determine experience level.
        Iterates levels from highest to lowest so overlapping ranges
        resolve to the most senior applicable level.
        """
        years = self._calculate_experience_years(text)
        levels = self.field_config.get("experience_levels", {})

        if not levels:
            if years == 0:
                return "Entry Level"
            elif years < 3:
                return "Junior"
            elif years < 7:
                return "Mid-Level"
            else:
                return "Senior"

        # Sort levels by min_years descending so senior is checked first
        sorted_levels = sorted(
            levels.items(),
            key=lambda item: item[1].get("min_years", 0),
            reverse=True,
        )

        for level_name, range_dict in sorted_levels:
            min_y = range_dict.get("min_years", 0)
            max_y = range_dict.get("max_years", 100)
            if min_y <= years <= max_y:
                return level_name.title()

        return "Unknown"

    def _determine_education_level(self, text: str) -> str:
        text_lower = text.lower()

        if re.search(r"\b(?:ph\.?d|doctorate|doctoral)\b", text_lower):
            return "PhD"
        if re.search(r"\b(?:master|m\.s\.|m\.a\.|mba|msc|m\.eng)\b", text_lower):
            return "Master's"
        if re.search(r"\b(?:bachelor|b\.s\.|b\.a\.|b\.tech|bsc|b\.eng|be\b)\b", text_lower):
            return "Bachelor's"
        if re.search(r"\b(?:associate|diploma|a\.s\.|a\.a\.)\b", text_lower):
            return "Associate/Diploma"

        return "Not specified"

    def _create_summary(self, text: str) -> str:
        """Return first ~600 characters as a summary"""
        summary = " ".join(text.split())[:600]
        if len(text) > 600:
            summary += "…"
        return summary
