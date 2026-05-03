"""
Field-specific configurations for different industries.
Includes Pakistan-specific fields.
"""

FIELD_CONFIGS = {
    "Software Engineering": {
        "skills": [
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
            "swift", "kotlin", "react", "angular", "vue", "node.js", "express",
            "django", "flask", "fastapi", "spring boot", "next.js", "nuxt.js", "svelte",
            "html", "css", "sass", "tailwind", "react native", "flutter", "ios", "android",
            "sql", "postgresql", "mysql", "mongodb", "redis", "cassandra", "elasticsearch",
            "dynamodb", "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "jenkins", "gitlab ci", "github actions", "ci/cd", "devops", "microservices",
            "serverless", "machine learning", "deep learning", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "data science", "nlp", "computer vision",
            "opencv", "git", "agile", "scrum", "rest api", "graphql", "websocket", "grpc",
        ],
        "certifications": [
            "aws certified", "azure certified", "google cloud certified",
            "certified kubernetes", "pmp", "csm", "cka", "ckad",
        ],
        "required_sections": ["skills", "experience", "projects"],
        "experience_levels": {
            "junior":  {"min_years": 0,  "max_years": 2},
            "mid":     {"min_years": 2,  "max_years": 5},
            "senior":  {"min_years": 5,  "max_years": 10},
            "lead":    {"min_years": 10, "max_years": 100},
        },
    },

    "Data Science & Analytics": {
        "skills": [
            "python", "r", "sql", "scala", "julia", "pandas", "numpy", "scipy",
            "statsmodels", "data analysis", "statistical analysis", "machine learning",
            "deep learning", "scikit-learn", "tensorflow", "pytorch", "keras",
            "xgboost", "lightgbm", "catboost", "nlp", "natural language processing",
            "computer vision", "opencv", "spacy", "nltk", "transformers", "bert", "gpt",
            "matplotlib", "seaborn", "plotly", "tableau", "power bi", "looker",
            "data visualization", "spark", "hadoop", "hive", "kafka", "airflow",
            "big data", "postgresql", "mongodb", "snowflake", "redshift", "bigquery",
            "aws", "azure", "gcp", "sagemaker", "azure ml", "vertex ai",
            "jupyter", "git", "a/b testing", "statistics", "probability",
        ],
        "certifications": [
            "google data analyst", "aws certified data analytics",
            "microsoft certified data scientist", "cloudera certified",
            "databricks certified",
        ],
        "required_sections": ["skills", "experience", "projects", "education"],
        "experience_levels": {
            "junior": {"min_years": 0,  "max_years": 2},
            "mid":    {"min_years": 2,  "max_years": 5},
            "senior": {"min_years": 5,  "max_years": 100},
        },
    },

    "Pharmacy": {
        "skills": [
            "pharmacology", "pharmaceutical", "drug therapy", "medication management",
            "clinical pharmacy", "pharmacy practice", "compounding", "dispensing",
            "drug interactions", "pharmacokinetics", "pharmacodynamics", "toxicology",
            "pharmaceutical care", "oncology pharmacy", "pediatric pharmacy",
            "geriatric pharmacy", "critical care pharmacy", "infectious diseases",
            "immunology", "nuclear pharmacy", "usp", "gmp", "quality assurance",
            "regulatory affairs", "fda guidelines", "drug safety", "pharmacovigilance",
            "adverse drug reactions", "patient counseling", "medication therapy management",
            "mtm", "clinical assessment", "drug information", "formulary management",
            "therapeutic drug monitoring", "pharmacy informatics", "ehr",
            "prescription processing", "inventory management", "clinical trials",
            "drug development", "pharmaceutical research", "biostatistics",
        ],
        "certifications": [
            "rph", "pharmd", "bcps", "bcacp", "bcop", "bcccp", "bcpps", "bcgp",
            "board certified", "pharmacy license", "controlled substance",
            "immunization certified",
        ],
        "required_sections": ["education", "licenses", "experience", "certifications"],
        "experience_levels": {
            "intern":            {"min_years": 0, "max_years": 1},
            "staff pharmacist":  {"min_years": 0, "max_years": 3},
            "clinical pharmacist": {"min_years": 2, "max_years": 5},
            "senior pharmacist": {"min_years": 5, "max_years": 100},
        },
    },

    "Teaching & Education": {
        "skills": [
            "lesson planning", "curriculum development", "classroom management",
            "differentiated instruction", "student assessment", "educational assessment",
            "formative assessment", "summative assessment", "pedagogy",
            "instructional design", "teaching strategies", "student engagement",
            "educational technology", "e-learning", "online teaching", "lms",
            "google classroom", "canvas", "moodle", "blackboard", "zoom",
            "microsoft teams", "mathematics", "science", "english", "social studies",
            "stem", "steam", "literacy", "numeracy", "critical thinking",
            "problem solving", "special education", "iep", "504 plan",
            "inclusive education", "learning disabilities", "gifted education",
            "esl", "ell", "bilingual education", "child development",
            "adolescent psychology", "behavior management", "social-emotional learning",
            "counseling", "mentoring", "parent communication", "educational research",
            "action research", "data-driven instruction", "professional development",
        ],
        "certifications": [
            "teaching license", "teaching credential", "state certification",
            "national board certification", "nbct", "tesol", "tefl",
            "montessori", "waldorf", "special education certification",
            "esl certification", "administrator license",
        ],
        "required_sections": ["education", "certifications", "experience"],
        "experience_levels": {
            "student teacher":   {"min_years": 0,  "max_years": 1},
            "new teacher":       {"min_years": 0,  "max_years": 3},
            "experienced teacher": {"min_years": 3, "max_years": 10},
            "master teacher":    {"min_years": 10, "max_years": 100},
        },
    },

    "Healthcare & Nursing": {
        "skills": [
            "patient care", "clinical assessment", "vital signs",
            "medication administration", "wound care", "iv therapy",
            "catheterization", "phlebotomy", "injections", "critical care",
            "emergency care", "pediatric care", "geriatric care", "oncology",
            "cardiac care", "icu", "er", "or", "labor and delivery", "nicu",
            "cpr", "bls", "acls", "pals", "first aid", "triage",
            "ventilator management", "patient monitoring", "life support",
            "medical records", "electronic health records", "ehr", "emr",
            "epic", "cerner", "charting", "documentation", "care plans",
            "case management", "discharge planning", "patient education",
            "care coordination", "interdisciplinary collaboration",
            "infection control", "patient safety", "quality improvement",
            "hipaa", "joint commission",
        ],
        "certifications": [
            "rn", "lpn", "bsn", "msn", "dnp", "ccrn", "cen", "cnor",
            "crna", "np", "fnp", "bls", "acls", "pals", "cpr certified",
            "nursing license", "board certified",
        ],
        "required_sections": ["licenses", "certifications", "clinical experience", "education"],
        "experience_levels": {
            "new graduate":      {"min_years": 0, "max_years": 1},
            "staff nurse":       {"min_years": 1, "max_years": 3},
            "experienced nurse": {"min_years": 3, "max_years": 7},
            "senior nurse":      {"min_years": 7, "max_years": 100},
        },
    },

    "Mechanical Engineering": {
        "skills": [
            "mechanical design", "cad", "autocad", "solidworks", "catia", "creo",
            "inventor", "3d modeling", "technical drawing", "gd&t",
            "tolerance analysis", "fea", "finite element analysis", "ansys",
            "abaqus", "nastran", "cfd", "computational fluid dynamics",
            "stress analysis", "thermal analysis", "vibration analysis",
            "manufacturing processes", "machining", "cnc", "casting", "welding",
            "sheet metal", "injection molding", "additive manufacturing",
            "3d printing", "rapid prototyping", "materials science", "metallurgy",
            "composites", "polymers", "material selection", "hvac",
            "thermodynamics", "heat transfer", "fluid mechanics", "mechanics",
            "kinematics", "dynamics", "control systems", "mechatronics", "robotics",
            "plm", "pdm", "asme", "iso", "lean manufacturing", "six sigma",
            "dfm", "dfa", "project management", "product development", "r&d",
        ],
        "certifications": [
            "pe", "professional engineer", "fe", "eit", "cswp", "cswa",
            "solidworks certified", "six sigma", "pmp", "asme certified",
        ],
        "required_sections": ["education", "technical skills", "projects", "experience"],
        "experience_levels": {
            "entry level":       {"min_years": 0,  "max_years": 2},
            "engineer":          {"min_years": 2,  "max_years": 5},
            "senior engineer":   {"min_years": 5,  "max_years": 10},
            "principal engineer": {"min_years": 10, "max_years": 100},
        },
    },

    "Marketing & Sales": {
        "skills": [
            "digital marketing", "seo", "sem", "google ads", "facebook ads",
            "social media marketing", "content marketing", "email marketing",
            "marketing automation", "hubspot", "marketo", "google analytics",
            "marketing analytics", "data analysis", "a/b testing",
            "conversion optimization", "roi analysis", "kpi tracking",
            "web analytics", "copywriting", "content creation", "storytelling",
            "brand development", "creative strategy", "video marketing",
            "graphic design", "adobe creative suite", "sales", "lead generation",
            "prospecting", "cold calling", "crm", "salesforce", "account management",
            "b2b sales", "b2c sales", "negotiation", "closing",
            "marketing strategy", "go-to-market strategy", "market research",
            "competitor analysis", "customer segmentation", "positioning",
            "brand management", "social media", "linkedin", "instagram",
            "facebook", "tiktok", "wordpress", "shopify",
        ],
        "certifications": [
            "google ads certified", "google analytics certified",
            "hubspot certified", "facebook blueprint", "hootsuite certified",
            "salesforce certified",
        ],
        "required_sections": ["experience", "achievements", "campaigns"],
        "experience_levels": {
            "coordinator": {"min_years": 0,  "max_years": 2},
            "specialist":  {"min_years": 2,  "max_years": 5},
            "manager":     {"min_years": 5,  "max_years": 10},
            "director":    {"min_years": 10, "max_years": 100},
        },
    },

    "Finance & Accounting": {
        "skills": [
            "accounting", "bookkeeping", "financial reporting", "gaap", "ifrs",
            "sox compliance", "accounts payable", "accounts receivable",
            "general ledger", "reconciliation", "financial analysis",
            "financial modeling", "forecasting", "budgeting", "variance analysis",
            "valuation", "dcf", "financial planning", "fp&a", "excel",
            "quickbooks", "sap", "oracle financials", "netsuite",
            "microsoft dynamics", "tableau", "power bi", "sql",
            "tax preparation", "tax planning", "audit", "internal audit",
            "external audit", "risk management", "compliance",
            "investment banking", "equity research", "portfolio management",
            "trading", "derivatives", "fixed income", "mergers and acquisitions",
        ],
        "certifications": [
            "cpa", "cfa", "cma", "cia", "ea", "cfp", "frm", "acca", "caia",
        ],
        "required_sections": ["education", "certifications", "experience"],
        "experience_levels": {
            "staff accountant":    {"min_years": 0,  "max_years": 2},
            "senior accountant":   {"min_years": 2,  "max_years": 5},
            "accounting manager":  {"min_years": 5,  "max_years": 10},
            "controller":          {"min_years": 10, "max_years": 100},
        },
    },

    # ======================================================= #
    #  PAKISTAN-SPECIFIC FIELDS                               #
    # ======================================================= #

    "Medical & MBBS": {
        "skills": [
            "clinical examination", "history taking", "patient diagnosis",
            "differential diagnosis", "treatment planning", "mbbs", "medicine",
            "surgery", "pediatrics", "gynecology", "obstetrics", "psychiatry",
            "dermatology", "cardiology", "neurology", "orthopedics", "ophthalmology",
            "ent", "radiology", "pathology", "pharmacology", "anatomy", "physiology",
            "biochemistry", "community medicine", "forensic medicine",
            "emergency medicine", "icu management", "cpr", "bls", "acls",
            "ecg interpretation", "ultrasound", "lab interpretation",
            "medical ethics", "patient counseling", "ward management",
            "outpatient clinic", "inpatient management", "referral system",
            "pmdc registered", "house job", "fcps", "mcps",
        ],
        "certifications": [
            "mbbs", "fcps", "mcps", "pmdc", "pmdc registration",
            "bls certified", "acls certified", "pals certified",
            "diploma in medicine", "md", "ms surgery", "dgo",
        ],
        "required_sections": ["education", "pmdc registration", "experience", "rotations"],
        "experience_levels": {
            "medical student":  {"min_years": 0, "max_years": 0},
            "house officer":    {"min_years": 0, "max_years": 1},
            "medical officer":  {"min_years": 1, "max_years": 4},
            "specialist":       {"min_years": 4, "max_years": 10},
            "consultant":       {"min_years": 10, "max_years": 100},
        },
    },

    "Law & Legal": {
        "skills": [
            "legal research", "legal drafting", "contract drafting",
            "litigation", "civil litigation", "criminal litigation",
            "constitutional law", "corporate law", "family law",
            "property law", "criminal law", "contract law", "tort law",
            "intellectual property", "tax law", "labour law",
            "banking law", "arbitration", "mediation", "negotiation",
            "court proceedings", "filing petitions", "bar council",
            "pakistan penal code", "ppc", "crpc", "civil procedure code",
            "cpc", "family courts act", "guardian courts",
            "advocate high court", "supreme court practice",
            "legal due diligence", "mergers and acquisitions",
            "legal compliance", "regulatory affairs", "legal advisory",
            "writ petitions", "appeals", "review petitions",
            "client counseling", "legal opinion writing",
        ],
        "certifications": [
            "llb", "llm", "bar council enrollment", "advocate",
            "advocate high court", "advocate supreme court",
            "pbcl enrolled", "pbcl certificate",
        ],
        "required_sections": ["education", "bar enrollment", "experience", "specializations"],
        "experience_levels": {
            "law student":    {"min_years": 0, "max_years": 0},
            "junior advocate":{"min_years": 0, "max_years": 3},
            "advocate":       {"min_years": 3, "max_years": 7},
            "senior advocate":{"min_years": 7, "max_years": 15},
            "principal":      {"min_years": 15, "max_years": 100},
        },
    },

    "Civil Engineering": {
        "skills": [
            "structural design", "rcc design", "steel design", "foundation design",
            "retaining walls", "bridge design", "road design", "highway engineering",
            "transportation engineering", "geotechnical engineering", "soil testing",
            "site investigation", "construction management", "project management",
            "quantity surveying", "bill of quantities", "boq", "cost estimation",
            "autocad", "civil 3d", "etabs", "staad pro", "sap2000",
            "primavera p6", "ms project", "revit", "safe", "matlab",
            "land surveying", "gps surveying", "total station", "leveling",
            "irrigation engineering", "water supply", "sewerage design",
            "hydraulics", "hydrology", "environmental engineering",
            "construction supervision", "quality control", "qc",
            "nespak", "pec registered", "nha", "wapda", "kda", "nca",
            "building codes", "neqs", "environmental impact assessment", "eia",
        ],
        "certifications": [
            "pec registered engineer", "pec", "b.e civil", "b.sc civil",
            "m.sc structures", "m.sc transportation", "pe license",
            "project management professional", "pmp", "six sigma",
        ],
        "required_sections": ["education", "pec registration", "projects", "experience"],
        "experience_levels": {
            "graduate engineer": {"min_years": 0, "max_years": 2},
            "engineer":          {"min_years": 2, "max_years": 5},
            "senior engineer":   {"min_years": 5, "max_years": 10},
            "principal engineer":{"min_years": 10, "max_years": 100},
        },
    },

    "Business Administration": {
        "skills": [
            "business strategy", "strategic planning", "operations management",
            "supply chain management", "procurement", "vendor management",
            "human resource management", "hrm", "recruitment", "performance management",
            "organizational development", "od", "training and development",
            "financial management", "budgeting", "cost control", "p&l management",
            "business development", "client relationship management", "crm",
            "project management", "pmp", "agile", "business analysis",
            "market research", "feasibility study", "business plan writing",
            "ms office", "excel", "powerpoint", "erp systems", "sap", "oracle",
            "import export", "customs clearance", "trade finance", "lc",
            "iso 9001", "quality management", "total quality management", "tqm",
            "corporate governance", "compliance", "risk management",
            "team leadership", "stakeholder management", "negotiation",
            "presentation skills", "communication skills",
        ],
        "certifications": [
            "mba", "bba", "pgdm", "pmp", "six sigma green belt",
            "six sigma black belt", "cips", "shrm", "chartered accountant",
            "acca", "cma", "iso lead auditor",
        ],
        "required_sections": ["education", "experience", "achievements"],
        "experience_levels": {
            "assistant manager":  {"min_years": 0,  "max_years": 2},
            "manager":            {"min_years": 2,  "max_years": 5},
            "senior manager":     {"min_years": 5,  "max_years": 10},
            "general manager":    {"min_years": 10, "max_years": 100},
        },
    },

    "Textile & Fashion": {
        "skills": [
            "textile engineering", "fabric production", "yarn manufacturing",
            "weaving", "knitting", "dyeing", "printing", "finishing",
            "quality control", "fabric testing", "gsm testing", "tensile strength",
            "color fastness", "aatcc", "iso testing", "astm standards",
            "fashion design", "pattern making", "garment construction",
            "sewing", "stitching", "cutting", "grading", "marker making",
            "cad pattern", "gerber", "lectra", "optitex",
            "merchandising", "fashion merchandising", "production planning",
            "costing", "sourcing", "import export", "buying",
            "compliance", "social compliance", "oeko-tex", "gots",
            "sustainable fashion", "technical design", "tech pack",
            "fashion illustration", "adobe illustrator", "photoshop",
            "retail management", "visual merchandising", "brand management",
            "export documentation", "woven", "denim", "knitwear", "home textile",
        ],
        "certifications": [
            "b.sc textile engineering", "be textile", "m.sc textile",
            "fashion design diploma", "aita", "textile testing certification",
            "oeko-tex certification", "gots certification",
        ],
        "required_sections": ["education", "technical skills", "experience", "projects"],
        "experience_levels": {
            "trainee":           {"min_years": 0, "max_years": 1},
            "executive":         {"min_years": 1, "max_years": 3},
            "senior executive":  {"min_years": 3, "max_years": 6},
            "manager":           {"min_years": 6, "max_years": 100},
        },
    },
}

# ------------------------------------------------------------- #
#  Default weights per field                                     #
# ------------------------------------------------------------- #
DEFAULT_WEIGHTS = {
    "Software Engineering":       {"education": 15, "experience": 35, "skills": 30, "projects": 15, "certifications": 5},
    "Data Science & Analytics":   {"education": 25, "experience": 30, "skills": 25, "projects": 15, "certifications": 5},
    "Pharmacy":                   {"education": 30, "experience": 25, "skills": 15, "projects": 0,  "certifications": 30},
    "Teaching & Education":       {"education": 30, "experience": 30, "skills": 15, "projects": 0,  "certifications": 25},
    "Healthcare & Nursing":       {"education": 15, "experience": 30, "skills": 10, "projects": 0,  "certifications": 45},
    "Mechanical Engineering":     {"education": 25, "experience": 30, "skills": 25, "projects": 15, "certifications": 5},
    "Marketing & Sales":          {"education": 10, "experience": 35, "skills": 25, "projects": 20, "certifications": 10},
    "Finance & Accounting":       {"education": 25, "experience": 30, "skills": 15, "projects": 0,  "certifications": 30},
    "Medical & MBBS":  {"education": 35, "experience": 25, "skills": 20, "projects": 0,  "certifications": 20},
    "Law & Legal":     {"education": 30, "experience": 35, "skills": 20, "projects": 0,  "certifications": 15},
    "Civil Engineering": {"education": 25, "experience": 30, "skills": 25, "projects": 15, "certifications": 5},
    "Business Administration": {"education": 20, "experience": 35, "skills": 25, "projects": 10, "certifications": 10},
    "Textile & Fashion": {"education": 20, "experience": 35, "skills": 30, "projects": 10, "certifications": 5},
}


def get_field_config(field_name: str) -> dict:
    return FIELD_CONFIGS.get(field_name, FIELD_CONFIGS["Software Engineering"])


def get_default_weights(field_name: str) -> dict:
    return DEFAULT_WEIGHTS.get(field_name, DEFAULT_WEIGHTS["Software Engineering"])


def get_all_fields() -> list:
    return list(FIELD_CONFIGS.keys())
