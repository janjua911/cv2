import streamlit as st
import os
from utils.cv_processor import CVProcessor
from utils.rag_engine import RAGEngine
import json

# Page configuration
st.set_page_config(
    page_title="CV Screening RAG System",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine()
if 'cvs_processed' not in st.session_state:
    st.session_state.cvs_processed = False

def main():
    st.title("📄 AI-Powered CV Screening System")
    st.markdown("### Upload CVs and find the perfect candidate using AI")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Project Info")
        st.info("""
        **RAG-Based CV Matcher**
        
        This system uses:
        - 🤖 Sentence Transformers for embeddings
        - 🗄️ ChromaDB for vector storage
        - 🔍 RAG for intelligent matching
        
        Upload CVs and query with natural language!
        """)
        
        if st.button("🗑️ Clear All CVs"):
            st.session_state.rag_engine.clear_database()
            st.session_state.cvs_processed = False
            st.success("Database cleared!")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload CVs", "🔍 Search Candidates", "📊 View All CVs"])
    
    # Tab 1: Upload CVs
    with tab1:
        st.header("Upload Candidate CVs")
        
        uploaded_files = st.file_uploader(
            "Upload CV files (PDF, TXT, or DOCX)",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Process CVs"):
                with st.spinner("Processing CVs..."):
                    cv_processor = CVProcessor()
                    
                    for uploaded_file in uploaded_files:
                        # Save file temporarily
                        file_path = os.path.join("data/cvs", uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process CV
                        cv_data = cv_processor.process_cv(file_path, uploaded_file.name)
                        
                        # Add to RAG engine
                        st.session_state.rag_engine.add_cv(cv_data)
                    
                    st.session_state.cvs_processed = True
                    st.success(f"✅ Successfully processed {len(uploaded_files)} CVs!")
    
    # Tab 2: Search candidates
    with tab2:
        st.header("Find the Perfect Candidate")
        
        if not st.session_state.cvs_processed:
            st.warning("⚠️ Please upload and process CVs first in the 'Upload CVs' tab.")
        else:
            st.markdown("### Enter your requirements")
            
            query = st.text_area(
                "What kind of candidate are you looking for?",
                placeholder="Example: I need a Python developer with 3+ years experience in machine learning and Django",
                height=100
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                top_k = st.number_input("Top candidates to show", min_value=1, max_value=10, value=3)
            
            if st.button("🔍 Search Candidates", type="primary"):
                if query:
                    with st.spinner("Searching..."):
                        results = st.session_state.rag_engine.search_candidates(query, top_k=top_k)
                        
                        st.markdown("### 🎯 Top Matching Candidates")
                        
                        for i, result in enumerate(results, 1):
                            with st.expander(f"#{i} - {result['name']} (Match Score: {result['score']:.2%})"):
                                col1, col2 = st.columns([2, 3])
                                
                                with col1:
                                    st.markdown("**📧 Contact:**")
                                    st.write(f"Email: {result['email']}")
                                    st.write(f"Phone: {result['phone']}")
                                    
                                    st.markdown("**💼 Skills:**")
                                    st.write(", ".join(result['skills'][:10]))
                                
                                with col2:
                                    st.markdown("**📄 Relevant Experience:**")
                                    st.write(result['summary'])
                                    
                                    st.markdown("**🎓 Education:**")
                                    st.write(result['education'])
                                
                                st.markdown("**📝 Why this candidate matches:**")
                                st.info(result['match_reason'])
                else:
                    st.error("Please enter a search query!")
    
    # Tab 3: View all CVs
    with tab3:
        st.header("All Uploaded CVs")
        
        if not st.session_state.cvs_processed:
            st.warning("⚠️ No CVs uploaded yet.")
        else:
            all_cvs = st.session_state.rag_engine.get_all_cvs()
            
            st.markdown(f"**Total CVs in database: {len(all_cvs)}**")
            
            for i, cv in enumerate(all_cvs, 1):
                with st.expander(f"{i}. {cv['name']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Contact Information:**")
                        st.write(f"📧 Email: {cv['email']}")
                        st.write(f"📱 Phone: {cv['phone']}")
                        
                        st.markdown("**Skills:**")
                        st.write(", ".join(cv['skills']))
                    
                    with col2:
                        st.markdown("**Education:**")
                        st.write(cv['education'])
                        
                        st.markdown("**Summary:**")
                        st.write(cv['summary'])

if __name__ == "__main__":
    main()
