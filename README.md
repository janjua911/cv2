# 📄 AI-Powered CV Screening System using RAG

A Machine Learning project that uses **Retrieval-Augmented Generation (RAG)** to intelligently match candidate CVs with job requirements.

## 🎯 Project Overview

This project demonstrates a practical application of RAG technology for HR and recruitment. It allows you to:
- Upload multiple candidate CVs (PDF, DOCX, TXT)
- Query the system with natural language job requirements
- Get ranked candidates based on semantic similarity
- View detailed match explanations

## 🏗️ Architecture

```
CV Upload → Text Extraction → Sentence Embeddings → ChromaDB Vector Store
                                                              ↓
User Query → Query Embedding → Semantic Search → Ranked Results
```

### Key Components:

1. **CV Processor**: Extracts text and structured data from CVs
2. **RAG Engine**: Creates embeddings and performs semantic search
3. **Vector Database**: ChromaDB stores CV embeddings
4. **Embedding Model**: Sentence-Transformers (all-MiniLM-L6-v2)
5. **UI**: Streamlit web interface

## 🚀 Technology Stack

- **Python 3.8+**
- **Streamlit** - Web UI
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embedding model
- **PyPDF2 & python-docx** - Document processing

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- 2GB free disk space (for models)

## 🔧 Installation

### Step 1: Clone the project
```bash
cd cv_rag_project
```

### Step 2: Create virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Start the application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### How to use:

1. **Upload CVs Tab**:
   - Click "Browse files" and select CV files (PDF/DOCX/TXT)
   - Click "Process CVs" button
   - Wait for processing to complete

2. **Search Candidates Tab**:
   - Enter your job requirements in natural language
   - Example: "I need a Python developer with 3+ years experience in machine learning"
   - Select number of top candidates to show
   - Click "Search Candidates"
   - Review matched candidates with scores

3. **View All CVs Tab**:
   - See all uploaded CVs
   - Review candidate information

## 📁 Project Structure

```
cv_rag_project/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── utils/
│   ├── __init__.py
│   ├── cv_processor.py        # CV text extraction & parsing
│   └── rag_engine.py          # RAG logic & vector search
│
├── data/
│   ├── cvs/                   # Uploaded CV files (sample CVs included)
│   └── chroma_db/             # ChromaDB vector database
│
└── models/                    # Downloaded embedding models (auto-created)
```

## 🧪 Sample CVs Included

The project includes 5 sample CVs for testing:
1. Hassan Ahmed - Software Engineer (Python, ML, Django)
2. Adnan Malik - Data Scientist (NLP, Deep Learning)
3. Talha Khan - Full Stack Developer (React, Node.js)
4. Usman Ali - Mobile Developer (React Native, Flutter)
5. Bilal Raza - DevOps Engineer (AWS, Kubernetes, Docker)

## 🔍 Example Queries

Try these example queries:

```
"I need a Python developer with machine learning experience"
"Find me a full stack developer with React and Node.js skills"
"Looking for someone with AWS and DevOps experience"
"Need a mobile app developer familiar with React Native"
"Find a data scientist with NLP experience"
```

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Building a RAG system from scratch
- ✅ Using vector embeddings for semantic search
- ✅ Document processing and information extraction
- ✅ Vector database operations (ChromaDB)
- ✅ Creating practical ML applications
- ✅ Building interactive UI with Streamlit

## 🔧 Customization

### Change Embedding Model:
Edit `utils/rag_engine.py`:
```python
self.model = SentenceTransformer('all-mpnet-base-v2')  # More accurate
# or
self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Faster
```

### Add More Skills:
Edit `utils/cv_processor.py` and add to `skills_keywords` list

### Adjust Search Results:
In the Search tab, change the `top_k` parameter

## 🐛 Troubleshooting

### Issue: "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### Issue: ChromaDB errors
```bash
# Clear the database
rm -rf data/chroma_db/
# Restart the app
```

### Issue: PDF extraction fails
```bash
pip install --upgrade PyPDF2
```

## 📊 Performance

- **Embedding Model Size**: ~80MB
- **Average Processing Time**: 2-3 seconds per CV
- **Search Speed**: <1 second for 100 CVs
- **Accuracy**: Depends on query quality and CV content

## 🚀 Future Enhancements

Potential improvements:
- [ ] Add support for more file formats (ODT, RTF)
- [ ] Implement advanced filtering (experience years, location)
- [ ] Add resume scoring system
- [ ] Export results to CSV/PDF
- [ ] Multi-language support
- [ ] Integration with ATS systems
- [ ] API endpoint for external applications

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

**Your Name**
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]
- Email: your.email@example.com

## 🙏 Acknowledgments

- Sentence Transformers by UKPLab
- ChromaDB by Chroma
- Streamlit by Streamlit Inc.
- LangChain community

## 📮 Contact

For questions or feedback, please open an issue on GitHub or contact me directly.

---

**Made with ❤️ for the ML/AI community**
