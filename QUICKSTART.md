# 🚀 Quick Start Guide

## Installation (3 Steps)

### Method 1: Automatic (Recommended)

**On Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**On Windows:**
```bash
run.bat
```

### Method 2: Manual

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate virtual environment:**

On Windows:
```bash
venv\Scripts\activate
```

On Mac/Linux:
```bash
source venv/bin/activate
```

3. **Install dependencies & run:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

## First-Time Usage

1. Open browser at `http://localhost:8501`
2. Go to "Upload CVs" tab
3. Upload sample CVs from `data/cvs/` folder (5 CVs included)
4. Click "Process CVs"
5. Go to "Search Candidates" tab
6. Try this query: `"Python developer with machine learning experience"`
7. See matched candidates!

## Sample Queries to Try

```
"I need a full stack developer with React and Node.js"
"Find me someone with AWS and DevOps skills"
"Looking for a mobile developer with React Native"
"Data scientist with NLP experience"
"Python engineer with 3+ years experience"
```

## Troubleshooting

**Error: Module not found**
```bash
pip install --upgrade -r requirements.txt
```

**Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Database errors**
```bash
rm -rf data/chroma_db/
# Restart the app
```

## Project Demo for Portfolio

1. Record screen while using the app
2. Show CV upload process
3. Demonstrate different queries
4. Explain the RAG architecture
5. Show code structure

## Next Steps

- Add your own CVs
- Modify for your specific use case
- Deploy to cloud (Streamlit Cloud, Heroku)
- Add to your GitHub portfolio
- Include in resume/LinkedIn

---
Need help? Check the main README.md file!
