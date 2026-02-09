"""
Test script to verify the CV RAG system works correctly
Run this before using the Streamlit app
"""

import sys
import os

print("=" * 50)
print("CV RAG System - Test Script")
print("=" * 50)
print()

# Test 1: Check Python version
print("Test 1: Checking Python version...")
if sys.version_info < (3, 8):
    print("❌ Python 3.8+ required. Current:", sys.version)
    sys.exit(1)
print(f"✅ Python version: {sys.version.split()[0]}")
print()

# Test 2: Check dependencies
print("Test 2: Checking dependencies...")
required_packages = [
    'streamlit',
    'langchain',
    'sentence_transformers',
    'chromadb',
    'PyPDF2',
    'docx',
    'pandas'
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package}")
        missing_packages.append(package)

if missing_packages:
    print()
    print("⚠️  Missing packages. Install with:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
print()

# Test 3: Check directories
print("Test 3: Checking directories...")
required_dirs = ['data/cvs', 'utils']
for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"  ✅ {dir_path}")
    else:
        print(f"  ❌ {dir_path} not found")
        os.makedirs(dir_path, exist_ok=True)
        print(f"     Created {dir_path}")
print()

# Test 4: Check sample CVs
print("Test 4: Checking sample CVs...")
cv_dir = 'data/cvs'
if os.path.exists(cv_dir):
    cv_files = [f for f in os.listdir(cv_dir) if f.endswith(('.txt', '.pdf', '.docx'))]
    print(f"  ✅ Found {len(cv_files)} CV files")
    for cv_file in cv_files[:5]:  # Show first 5
        print(f"     - {cv_file}")
else:
    print("  ⚠️  No CV directory found")
print()

# Test 5: Test CV Processor
print("Test 5: Testing CV Processor...")
try:
    from utils.cv_processor import CVProcessor
    processor = CVProcessor()
    print("  ✅ CV Processor imported successfully")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)
print()

# Test 6: Test RAG Engine
print("Test 6: Testing RAG Engine...")
try:
    from utils.rag_engine import RAGEngine
    print("  ⏳ Initializing RAG Engine (downloading model if needed)...")
    engine = RAGEngine()
    print("  ✅ RAG Engine initialized successfully")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)
print()

# Test 7: Quick functional test
print("Test 7: Running functional test...")
try:
    # Process a sample CV if available
    if cv_files:
        sample_cv = os.path.join(cv_dir, cv_files[0])
        print(f"  Processing: {cv_files[0]}")
        
        cv_data = processor.process_cv(sample_cv, cv_files[0])
        print(f"  ✅ Extracted name: {cv_data['name']}")
        print(f"  ✅ Found {len(cv_data['skills'])} skills")
        
        # Test adding to RAG engine
        engine.add_cv(cv_data)
        print("  ✅ Added CV to vector database")
        
        # Test search
        results = engine.search_candidates("Python developer", top_k=1)
        print(f"  ✅ Search returned {len(results)} results")
    else:
        print("  ⚠️  No CV files to test with")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# All tests passed
print("=" * 50)
print("✅ ALL TESTS PASSED!")
print("=" * 50)
print()
print("You can now run the application:")
print("  streamlit run app.py")
print()
