"""
Field-specific configurations for different industries
Each field has custom skills, certifications, and scoring criteria
"""

FIELD_CONFIGS = {
    "Software Engineering": {
        "skills": [
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "swift", "kotlin",
            # Web Technologies
            "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi", "spring boot",
            "next.js", "nuxt.js", "svelte", "html", "css", "sass", "tailwind",
            # Mobile Development
            "react native", "flutter", "ios", "android", "xamarin",
            # Databases
            "sql", "postgresql", "mysql", "mongodb", "redis", "cassandra", "elasticsearch", "dynamodb",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "gitlab ci", "github actions",
            "ci/cd", "devops", "microservices", "serverless",
            # Data & AI
            "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
            "data science", "nlp", "computer vision", "opencv",
            # Other
            "git", "agile", "scrum", "rest api", "graphql", "websocket", "grpc"
        ],
        "certifications": [
            "aws certified", "azure certified", "google cloud certified", "certified kubernetes",
            "pmp", "csm", "cka", "ckad"
        ],
        "required_sections": ["skills", "experience", "projects"],
        "experience_levels": {
            "junior": {"min_years": 0, "max_years": 2},
            "mid": {"min_years": 2, "max_years": 5},
            "senior": {"min_years": 5, "max_years": 10},
            "lead": {"min_years": 10, "max_years": 100}
        }
    },
    
    "Data Science & Analytics": {
        "skills": [
            # Programming
            "python", "r", "sql", "scala", "julia",
            # Data Analysis
            "pandas", "numpy", "scipy", "statsmodels", "data analysis", "statistical analysis",
            # Machine Learning
            "machine learning", "deep learning", "scikit-learn", "tensorflow", "pytorch", "keras",
            "xgboost", "lightgbm", "catboost",
            # NLP & Computer Vision
            "nlp", "natural language processing", "computer vision", "opencv", "spacy", "nltk",
            "transformers", "bert", "gpt",
            # Visualization
            "matplotlib", "seaborn", "plotly", "tableau", "power bi", "looker", "data visualization",
            # Big Data
            "spark", "hadoop", "hive", "pig", "kafka", "airflow", "big data",
            # Databases
            "sql", "postgresql", "mongodb", "cassandra", "snowflake", "redshift", "bigquery",
            # Cloud
            "aws", "azure", "gcp", "sagemaker", "azure ml", "vertex ai",
            # Other
            "jupyter", "git", "a/b testing", "experimental design", "statistics", "probability"
        ],
        "certifications": [
            "google data analyst", "aws certified data analytics", "microsoft certified data scientist",
            "cloudera certified", "databricks certified"
        ],
        "required_sections": ["skills", "experience", "projects", "education"],
        "experience_levels": {
            "junior": {"min_years": 0, "max_years": 2},
            "mid": {"min_years": 2, "max_years": 5},
            "senior": {"min_years": 5, "max_years": 100}
        }
    },
    
    "Pharmacy": {
        "skills": [
            # Core Pharmacy
            "pharmacology", "pharmaceutical", "drug therapy", "medication management", "clinical pharmacy",
            "pharmacy practice", "compounding", "dispensing", "drug interactions", "pharmacokinetics",
            "pharmacodynamics", "toxicology", "pharmaceutical care",
            # Specializations
            "oncology pharmacy", "pediatric pharmacy", "geriatric pharmacy", "critical care pharmacy",
            "infectious diseases", "immunology", "nuclear pharmacy",
            # Regulatory & Quality
            "usp", "gmp", "quality assurance", "regulatory affairs", "fda guidelines", "ich guidelines",
            "drug safety", "pharmacovigilance", "adverse drug reactions",
            # Clinical Skills
            "patient counseling", "medication therapy management", "mtm", "clinical assessment",
            "drug information", "formulary management", "therapeutic drug monitoring",
            # Technology
            "pharmacy informatics", "electronic health records", "ehr", "pharmacy software",
            "prescription processing", "inventory management",
            # Research
            "clinical trials", "drug development", "pharmaceutical research", "biostatistics"
        ],
        "certifications": [
            "rph", "pharmd", "bcps", "bcacp", "bcop", "bcccp", "bcpps", "bcgp",
            "board certified", "pharmacy license", "controlled substance", "immunization certified"
        ],
        "required_sections": ["education", "licenses", "experience", "certifications"],
        "experience_levels": {
            "intern": {"min_years": 0, "max_years": 1},
            "staff pharmacist": {"min_years": 0, "max_years": 3},
            "clinical pharmacist": {"min_years": 2, "max_years": 5},
            "senior pharmacist": {"min_years": 5, "max_years": 100}
        }
    },
    
    "Teaching & Education": {
        "skills": [
            # Teaching Methods
            "lesson planning", "curriculum development", "classroom management", "differentiated instruction",
            "student assessment", "educational assessment", "formative assessment", "summative assessment",
            "pedagogy", "instructional design", "teaching strategies", "student engagement",
            # Technology
            "educational technology", "e-learning", "online teaching", "lms", "google classroom",
            "canvas", "moodle", "blackboard", "zoom", "microsoft teams", "interactive whiteboard",
            # Subject Areas
            "mathematics", "science", "english", "social studies", "stem", "steam", "literacy",
            "numeracy", "critical thinking", "problem solving",
            # Special Education
            "special education", "iep", "504 plan", "inclusive education", "learning disabilities",
            "gifted education", "esl", "ell", "bilingual education",
            # Student Development
            "child development", "adolescent psychology", "behavior management", "social-emotional learning",
            "counseling", "mentoring", "parent communication",
            # Research & Development
            "educational research", "action research", "data-driven instruction", "professional development"
        ],
        "certifications": [
            "teaching license", "teaching credential", "state certification", "national board certification",
            "nbct", "tesol", "tefl", "montessori", "waldorf", "special education certification",
            "esl certification", "administrator license", "principal license"
        ],
        "required_sections": ["education", "certifications", "teaching experience", "philosophy"],
        "experience_levels": {
            "student teacher": {"min_years": 0, "max_years": 1},
            "new teacher": {"min_years": 0, "max_years": 3},
            "experienced teacher": {"min_years": 3, "max_years": 10},
            "master teacher": {"min_years": 10, "max_years": 100}
        }
    },
    
    "Healthcare & Nursing": {
        "skills": [
            # Clinical Skills
            "patient care", "clinical assessment", "vital signs", "medication administration",
            "wound care", "iv therapy", "catheterization", "phlebotomy", "injections",
            # Specializations
            "critical care", "emergency care", "pediatric care", "geriatric care", "oncology",
            "cardiac care", "icu", "er", "or", "labor and delivery", "nicu",
            # Procedures
            "cpr", "bls", "acls", "pals", "first aid", "triage", "ventilator management",
            "patient monitoring", "life support",
            # Documentation
            "medical records", "electronic health records", "ehr", "emr", "epic", "cerner",
            "charting", "documentation", "care plans",
            # Patient Management
            "case management", "discharge planning", "patient education", "care coordination",
            "interdisciplinary collaboration",
            # Quality & Safety
            "infection control", "patient safety", "quality improvement", "hipaa", "joint commission"
        ],
        "certifications": [
            "rn", "lpn", "bsn", "msn", "dnp", "ccrn", "cen", "cnor", "crna", "np", "fnp",
            "bls", "acls", "pals", "cpr certified", "nursing license", "board certified"
        ],
        "required_sections": ["licenses", "certifications", "clinical experience", "education"],
        "experience_levels": {
            "new graduate": {"min_years": 0, "max_years": 1},
            "staff nurse": {"min_years": 1, "max_years": 3},
            "experienced nurse": {"min_years": 3, "max_years": 7},
            "senior nurse": {"min_years": 7, "max_years": 100}
        }
    },
    
    "Mechanical Engineering": {
        "skills": [
            # Core Engineering
            "mechanical design", "cad", "autocad", "solidworks", "catia", "creo", "inventor",
            "3d modeling", "technical drawing", "gd&t", "tolerance analysis",
            # Analysis & Simulation
            "fea", "finite element analysis", "ansys", "abaqus", "nastran", "cfd",
            "computational fluid dynamics", "stress analysis", "thermal analysis", "vibration analysis",
            # Manufacturing
            "manufacturing processes", "machining", "cnc", "casting", "welding", "sheet metal",
            "injection molding", "additive manufacturing", "3d printing", "rapid prototyping",
            # Materials
            "materials science", "metallurgy", "composites", "polymers", "material selection",
            # Systems
            "hvac", "thermodynamics", "heat transfer", "fluid mechanics", "mechanics",
            "kinematics", "dynamics", "control systems", "mechatronics", "robotics",
            # Tools & Standards
            "plm", "pdm", "asme", "iso", "lean manufacturing", "six sigma", "dfm", "dfa",
            # Project Management
            "project management", "product development", "r&d", "testing", "prototyping"
        ],
        "certifications": [
            "pe", "professional engineer", "fe", "eit", "cswp", "cswa", "solidworks certified",
            "six sigma", "pmp", "asme certified"
        ],
        "required_sections": ["education", "technical skills", "projects", "experience"],
        "experience_levels": {
            "entry level": {"min_years": 0, "max_years": 2},
            "engineer": {"min_years": 2, "max_years": 5},
            "senior engineer": {"min_years": 5, "max_years": 10},
            "principal engineer": {"min_years": 10, "max_years": 100}
        }
    },
    
    "Marketing & Sales": {
        "skills": [
            # Digital Marketing
            "digital marketing", "seo", "sem", "google ads", "facebook ads", "social media marketing",
            "content marketing", "email marketing", "marketing automation", "hubspot", "marketo",
            # Analytics
            "google analytics", "marketing analytics", "data analysis", "a/b testing", "conversion optimization",
            "roi analysis", "kpi tracking", "web analytics",
            # Content & Creative
            "copywriting", "content creation", "storytelling", "brand development", "creative strategy",
            "video marketing", "graphic design", "adobe creative suite",
            # Sales
            "sales", "lead generation", "prospecting", "cold calling", "crm", "salesforce",
            "account management", "b2b sales", "b2c sales", "negotiation", "closing",
            # Strategy
            "marketing strategy", "go-to-market strategy", "market research", "competitor analysis",
            "customer segmentation", "positioning", "brand management",
            # Platforms
            "social media", "linkedin", "twitter", "instagram", "facebook", "tiktok",
            "wordpress", "shopify", "wix"
        ],
        "certifications": [
            "google ads certified", "google analytics certified", "hubspot certified",
            "facebook blueprint", "hootsuite certified", "salesforce certified"
        ],
        "required_sections": ["experience", "achievements", "campaigns"],
        "experience_levels": {
            "coordinator": {"min_years": 0, "max_years": 2},
            "specialist": {"min_years": 2, "max_years": 5},
            "manager": {"min_years": 5, "max_years": 10},
            "director": {"min_years": 10, "max_years": 100}
        }
    },
    
    "Finance & Accounting": {
        "skills": [
            # Accounting
            "accounting", "bookkeeping", "financial reporting", "gaap", "ifrs", "sox compliance",
            "accounts payable", "accounts receivable", "general ledger", "reconciliation",
            # Financial Analysis
            "financial analysis", "financial modeling", "forecasting", "budgeting", "variance analysis",
            "valuation", "dcf", "financial planning", "fp&a",
            # Software
            "excel", "quickbooks", "sap", "oracle financials", "netsuite", "microsoft dynamics",
            "tableau", "power bi", "sql",
            # Tax & Audit
            "tax preparation", "tax planning", "audit", "internal audit", "external audit",
            "risk management", "compliance",
            # Investment & Banking
            "investment banking", "equity research", "portfolio management", "trading",
            "derivatives", "fixed income", "mergers and acquisitions", "m&a"
        ],
        "certifications": [
            "cpa", "cfa", "cma", "cia", "ea", "cfp", "frm", "acca", "caia"
        ],
        "required_sections": ["education", "certifications", "experience"],
        "experience_levels": {
            "staff accountant": {"min_years": 0, "max_years": 2},
            "senior accountant": {"min_years": 2, "max_years": 5},
            "accounting manager": {"min_years": 5, "max_years": 10},
            "controller": {"min_years": 10, "max_years": 100}
        }
    }
}

# Default weights for different fields
DEFAULT_WEIGHTS = {
    "Software Engineering": {
        "education": 15,
        "experience": 35,
        "skills": 30,
        "projects": 15,
        "certifications": 5
    },
    "Data Science & Analytics": {
        "education": 25,
        "experience": 30,
        "skills": 25,
        "projects": 15,
        "certifications": 5
    },
    "Pharmacy": {
        "education": 30,
        "experience": 25,
        "skills": 15,
        "licenses": 20,
        "certifications": 10
    },
    "Teaching & Education": {
        "education": 30,
        "experience": 30,
        "certifications": 25,
        "skills": 10,
        "philosophy": 5
    },
    "Healthcare & Nursing": {
        "licenses": 25,
        "certifications": 25,
        "experience": 30,
        "education": 15,
        "skills": 5
    },
    "Mechanical Engineering": {
        "education": 25,
        "experience": 30,
        "skills": 25,
        "projects": 15,
        "certifications": 5
    },
    "Marketing & Sales": {
        "experience": 35,
        "achievements": 25,
        "skills": 20,
        "education": 10,
        "certifications": 10
    },
    "Finance & Accounting": {
        "certifications": 30,
        "experience": 30,
        "education": 25,
        "skills": 15
    }
}

def get_field_config(field_name):
    """Get configuration for a specific field"""
    return FIELD_CONFIGS.get(field_name, FIELD_CONFIGS["Software Engineering"])

def get_default_weights(field_name):
    """Get default weights for a specific field"""
    return DEFAULT_WEIGHTS.get(field_name, DEFAULT_WEIGHTS["Software Engineering"])

def get_all_fields():
    """Get list of all available fields"""
    return list(FIELD_CONFIGS.keys())
