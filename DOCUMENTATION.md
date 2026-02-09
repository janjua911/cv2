# 📚 Project Documentation - CV RAG System

## 📖 Table of Contents
1. [What is RAG?](#what-is-rag)
2. [System Architecture](#system-architecture)
3. [How It Works](#how-it-works)
4. [Code Walkthrough](#code-walkthrough)
5. [Key Concepts](#key-concepts)
6. [Deployment Guide](#deployment-guide)

---

## 🤖 What is RAG?

**RAG** = **Retrieval-Augmented Generation**

RAG combines two powerful techniques:
- **Retrieval**: Finding relevant information from a knowledge base
- **Generation**: Creating responses using that information

### Why RAG for CV Screening?

Traditional keyword matching fails because:
- "Machine Learning" ≠ "ML" (synonyms not matched)
- "Python Developer" might be written as "Software Engineer - Python"
- Context and semantic meaning are lost

RAG solves this by:
- Understanding **semantic similarity** (meaning, not just words)
- Matching concepts, not just exact phrases
- Ranking candidates by relevance

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                    (Streamlit Web App)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      CV PROCESSOR                            │
│  • Extracts text from PDF/DOCX/TXT                          │
│  • Parses information (name, skills, education)             │
│  • Cleans and structures data                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    EMBEDDING MODEL                           │
│        (Sentence-Transformers: all-MiniLM-L6-v2)            │
│  • Converts text to 384-dimensional vectors                 │
│  • Captures semantic meaning                                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   VECTOR DATABASE                            │
│                    (ChromaDB)                                │
│  • Stores CV embeddings                                     │
│  • Performs similarity search                               │
│  • Returns ranked results                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    SEARCH RESULTS                            │
│  • Top-K most similar CVs                                   │
│  • Match scores                                             │
│  • Explanation of matches                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ How It Works

### Step 1: CV Upload & Processing

```python
# User uploads CV file
uploaded_file = "Hassan_Ahmed_CV.pdf"

# CV Processor extracts text
text = extract_text_from_pdf(uploaded_file)

# Parse structured information
cv_data = {
    'name': 'Hassan Ahmed',
    'skills': ['Python', 'Machine Learning', 'Django'],
    'education': 'BS Computer Science, NUST',
    'experience': '4+ years as Software Engineer'
}
```

### Step 2: Creating Embeddings

```python
# Combine CV information into text
cv_text = """
Name: Hassan Ahmed
Skills: Python, Machine Learning, Django, TensorFlow
Education: BS Computer Science, NUST
Experience: 4+ years as Software Engineer
"""

# Convert to vector embedding (384 dimensions)
embedding = model.encode(cv_text)
# Output: [0.234, -0.123, 0.567, ..., 0.891]  (384 numbers)
```

**What are embeddings?**
- Numbers that represent meaning
- Similar concepts → similar numbers
- "Python developer" and "Software Engineer - Python" will have similar embeddings

### Step 3: Storing in Vector Database

```python
# Store in ChromaDB
collection.add(
    embeddings=[embedding],
    documents=[cv_text],
    metadatas=[cv_data],
    ids=['hassan_cv']
)
```

### Step 4: User Query

```python
# User searches for:
query = "I need a Python developer with machine learning experience"

# Convert query to embedding
query_embedding = model.encode(query)
# Output: [0.245, -0.134, 0.578, ..., 0.882]
```

### Step 5: Similarity Search

```python
# Find similar CVs using cosine similarity
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5  # Top 5 matches
)

# Results ranked by similarity:
# 1. Hassan Ahmed - 0.92 match
# 2. Adnan Malik - 0.87 match
# 3. Talha Khan - 0.65 match
```

**Similarity Calculation:**
```
Similarity = cosine_similarity(query_embedding, cv_embedding)
Score closer to 1 = better match
```

---

## 💻 Code Walkthrough

### 1. CV Processor (`utils/cv_processor.py`)

```python
class CVProcessor:
    def process_cv(self, file_path, filename):
        # Extract text based on file type
        text = self._extract_text(file_path)
        
        # Extract structured information
        return {
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'skills': self._extract_skills(text),
            'education': self._extract_education(text)
        }
```

**Key Methods:**
- `_extract_text()`: Reads PDF/DOCX/TXT files
- `_extract_skills()`: Finds technical skills using keywords
- `_extract_education()`: Locates education section
- `_extract_email()`: Uses regex to find email addresses

### 2. RAG Engine (`utils/rag_engine.py`)

```python
class RAGEngine:
    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize vector database
        self.collection = chromadb.create_collection("cv_collection")
    
    def add_cv(self, cv_data):
        # Create text representation
        cv_text = self._create_cv_text(cv_data)
        
        # Generate embedding
        embedding = self.model.encode(cv_text).tolist()
        
        # Store in database
        self.collection.add(
            embeddings=[embedding],
            documents=[cv_text],
            metadatas=[cv_data]
        )
    
    def search_candidates(self, query, top_k=5):
        # Encode query
        query_embedding = self.model.encode(query).tolist()
        
        # Search database
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return self._format_results(results)
```

### 3. Streamlit App (`app.py`)

```python
# Initialize RAG engine
rag_engine = RAGEngine()

# Upload tab
uploaded_files = st.file_uploader("Upload CVs")
if st.button("Process CVs"):
    for file in uploaded_files:
        cv_data = processor.process_cv(file)
        rag_engine.add_cv(cv_data)

# Search tab
query = st.text_area("Enter job requirements")
if st.button("Search"):
    results = rag_engine.search_candidates(query)
    display_results(results)
```

---

## 🧠 Key Concepts

### 1. **Vector Embeddings**
- Text → Numbers
- Captures semantic meaning
- Dimensionality: typically 384 or 768

### 2. **Cosine Similarity**
```
similarity = dot(vec1, vec2) / (||vec1|| * ||vec2||)
Range: -1 to 1 (we use 0 to 1)
```

### 3. **ChromaDB**
- Vector database optimized for similarity search
- Uses HNSW algorithm for fast retrieval
- Persistent storage

### 4. **Sentence Transformers**
- Pre-trained models for text embeddings
- Models: 
  - `all-MiniLM-L6-v2`: Fast, 80MB
  - `all-mpnet-base-v2`: Accurate, 420MB

---

## 🚀 Deployment Guide

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
- Go to https://streamlit.io/cloud
- Connect your GitHub account
- Select your repository
- Set main file: `app.py`
- Deploy!

### Deploy to Heroku

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

---

## 📊 Performance Optimization

### 1. **Batch Processing**
```python
# Process multiple CVs at once
embeddings = model.encode(cv_texts, batch_size=32)
```

### 2. **Caching**
```python
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
```

### 3. **Smaller Model**
Use `paraphrase-MiniLM-L3-v2` for faster processing

---

## 🎯 Use Cases

This RAG system can be adapted for:
1. **Recruitment**: Match candidates to job descriptions
2. **Document Search**: Find relevant documents
3. **Customer Support**: Match queries to knowledge base
4. **Legal**: Find similar cases or precedents
5. **Research**: Find related papers

---

## 📈 Metrics & Evaluation

### How to measure performance:

1. **Precision@K**: Of top K results, how many are relevant?
2. **Recall**: Did we find all relevant candidates?
3. **MRR** (Mean Reciprocal Rank): Where does first relevant result appear?

### Example Evaluation:
```python
# Manual evaluation
test_queries = [
    ("Python developer", ["Hassan", "Adnan"]),  # Expected matches
    ("DevOps engineer", ["Bilal"]),
]

for query, expected in test_queries:
    results = rag_engine.search_candidates(query, top_k=3)
    actual = [r['name'] for r in results]
    precision = len(set(expected) & set(actual)) / len(actual)
    print(f"Precision for '{query}': {precision}")
```

---

## 🔬 Advanced Topics

### 1. **Hybrid Search**
Combine vector search with keyword matching:
```python
# Vector similarity + BM25 keyword matching
final_score = 0.7 * vector_score + 0.3 * keyword_score
```

### 2. **Re-ranking**
Use a cross-encoder to re-rank top results:
```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = reranker.predict([(query, cv) for cv in top_results])
```

### 3. **Query Expansion**
Expand query with synonyms:
```python
# "Python developer" → "Python developer OR Software Engineer Python"
```

---

## 📚 Further Learning

**Recommended Resources:**
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [RAG Tutorial by LangChain](https://python.langchain.com/docs/use_cases/question_answering/)
- [Hugging Face Course](https://huggingface.co/course)

**Papers:**
- "Sentence-BERT" (Reimers & Gurevych, 2019)
- "Retrieval-Augmented Generation" (Lewis et al., 2020)

---

## 💡 Tips for Your Interview/Portfolio

When presenting this project:

1. **Explain the problem**: Traditional keyword matching limitations
2. **Show the solution**: RAG with semantic search
3. **Demonstrate**: Live demo with different queries
4. **Discuss tradeoffs**: Speed vs accuracy, model selection
5. **Mention improvements**: What you would add with more time

**Key talking points:**
- "I built this to understand RAG architecture"
- "Uses Sentence Transformers for embeddings"
- "ChromaDB for efficient vector storage"
- "Can handle 1000+ CVs with sub-second search"
- "Easily adaptable to other domains"

---

**Happy Learning! 🚀**
