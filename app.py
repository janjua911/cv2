import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import io
from collections import Counter

from utils.cv_processor import AdvancedCVProcessor
from utils.rag_engine import AdvancedRAGEngine
from utils.field_config import get_all_fields, get_default_weights

# ============================================================ #
#  PAGE CONFIGURATION                                           #
# ============================================================ #
st.set_page_config(
    page_title="CV Screening Pro – AI Recruitment Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================ #
#  THEME / CSS                                                  #
# ============================================================ #
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .main { background-color: #0e1117; }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        padding: 1rem 0;
        letter-spacing: -0.02em;
    }
    .sub-header { text-align: center; color: #a0a0a0; margin-bottom: 2rem; font-size: 1.1rem; }

    .modern-card {
        background: #1e1e2e;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,.3);
        border: 1px solid #313244;
        transition: all .3s;
    }
    .modern-card:hover { transform: translateY(-4px); border-color: #667eea; }

    .gradient-metric {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        transition: transform .3s;
    }
    .gradient-metric:hover { transform: translateY(-3px); }
    .gradient-metric-green  { background: linear-gradient(135deg, #00b09b, #96c93d); }
    .gradient-metric-orange { background: linear-gradient(135deg, #f2994a, #f2c94c); }
    .gradient-metric-blue   { background: linear-gradient(135deg, #1f77b4, #4a90e2); }

    .metric-value { font-size: 2rem; font-weight: 700; margin: .5rem 0; }
    .metric-label { font-size: .85rem; opacity: .9; text-transform: uppercase; letter-spacing: 1px; }

    .score-excellent { background: linear-gradient(135deg, #00b09b, #96c93d); color: white;
                       padding: 4px 12px; border-radius: 50px; font-weight: 600; }
    .score-good      { background: linear-gradient(135deg, #f2994a, #f2c94c); color: white;
                       padding: 4px 12px; border-radius: 50px; font-weight: 600; }
    .score-average   { background: linear-gradient(135deg, #eb3349, #f45c43); color: white;
                       padding: 4px 12px; border-radius: 50px; font-weight: 600; }

    [data-testid="stSidebar"] { background: #1a1a2e; border-right: 1px solid #313244; }

    .stTabs [data-baseweb="tab-list"] { gap: .5rem; background: #1e1e2e;
                                        padding: .5rem; border-radius: 12px; }
    .stTabs [data-baseweb="tab"]      { border-radius: 8px; padding: .5rem 1.2rem;
                                        font-weight: 500; color: #a0a0a0; }
    .stTabs [aria-selected="true"]    { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }

    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 1.5rem 0;
    }

    .info-box { background: #1e1e2e; border-radius: 16px; padding: 1.2rem;
                border-left: 5px solid #667eea; color: #e0e0e0; }

    .footer { text-align: center; padding: 2rem; color: #666; font-size: .85rem;
              border-top: 1px solid #313244; margin-top: 2rem; }

    p, li { color: #e0e0e0; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff; }

    [data-testid="stMetric"] { background: #1e1e2e; padding: 1rem;
                                border-radius: 12px; border: 1px solid #313244; }

    .stProgress > div > div { background: linear-gradient(135deg, #667eea, #764ba2); }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp .6s ease-out; }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================ #
#  HELPERS                                                      #
# ============================================================ #
def get_score_class(score: float) -> str:
    if score >= 75:
        return "score-excellent"
    elif score >= 55:
        return "score-good"
    return "score-average"


def get_score_emoji(score: float) -> str:
    if score >= 75:
        return "🏆"
    elif score >= 55:
        return "⭐"
    return "📌"


def clamp_score(score: float) -> float:
    """Ensure displayed score is in [0, 100]"""
    return min(max(score * 100, 0.0), 100.0)


def cvs_to_dataframe(cvs: list) -> pd.DataFrame:
    rows = []
    for cv in cvs:
        rows.append(
            {
                "Name": cv.get("name", ""),
                "Email": cv.get("email", ""),
                "Experience (yrs)": cv.get("years_of_experience", 0),
                "Level": cv.get("experience_level", ""),
                "Education": cv.get("education_level", ""),
                "Skills": ", ".join(cv.get("skills", [])[:10]),
                "Score (%)": round(clamp_score(cv.get("final_score", 0)), 1),
                "Match Reason": cv.get("match_reason", ""),
            }
        )
    return pd.DataFrame(rows)


# ============================================================ #
#  SESSION STATE INIT                                           #
# ============================================================ #
if "engine" not in st.session_state:
    with st.spinner("🚀 Initialising AI models – please wait…"):
        try:
            st.session_state.engine = AdvancedRAGEngine(
                model_name="all-mpnet-base-v2",
                use_reranker=True,
            )
            st.session_state.processed_cvs = []
            st.session_state.selected_field = "Software Engineering"
            st.session_state.search_results = []
            st.session_state.favorites = []
        except Exception as e:
            st.error(f"⚠️ Error initialising engine: {e}")
            st.session_state.engine = None

# ============================================================ #
#  SIDEBAR                                                      #
# ============================================================ #
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:1rem 0;">
            <div style="font-size:4rem;">🧑🏻‍🎓</div>
            <h2 style="color:#667eea;margin:0;">CV Screening Pro</h2>
            <p style="color:#888;font-size:.8rem;">AI-Powered Recruitment</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Industry ---
    st.markdown("### 🏭 Industry")
    all_fields = get_all_fields()
    selected_field = st.selectbox(
        "Select Industry",
        all_fields,
        index=all_fields.index(st.session_state.get("selected_field", all_fields[0])),
        label_visibility="collapsed",
    )
    # Persist selected field
    st.session_state.selected_field = selected_field

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Scoring Weights (load field-specific defaults) ---
    st.markdown("### ⚖️ Scoring Weights")
    field_defaults = get_default_weights(selected_field)
    # Ensure the five standard keys are always present with integer values
    default_weights = {
        "education": int(field_defaults.get("education", 20)),
        "experience": int(field_defaults.get("experience", 30)),
        "skills": int(field_defaults.get("skills", 30)),
        "projects": int(field_defaults.get("projects", 10)),
        "certifications": int(field_defaults.get("certifications", 10)),
    }
    # Normalise defaults so they sum to 100
    total_default = sum(default_weights.values()) or 100
    default_weights = {
        k: round(v * 100 / total_default) for k, v in default_weights.items()
    }

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        w_edu  = st.slider("🎓 Education",       0, 100, default_weights["education"],       5)
        w_exp  = st.slider("💼 Experience",       0, 100, default_weights["experience"],      5)
    with col_w2:
        w_ski  = st.slider("🔧 Skills",           0, 100, default_weights["skills"],          5)
        w_pro  = st.slider("📁 Projects",         0, 100, default_weights["projects"],        5)
        w_cer  = st.slider("📜 Certifications",   0, 100, default_weights["certifications"],  5)

    weights = {
        "education":      w_edu,
        "experience":     w_exp,
        "skills":         w_ski,
        "projects":       w_pro,
        "certifications": w_cer,
    }
    total_weight = sum(weights.values())
    if total_weight != 100:
        st.warning(f"⚠️ Weights total: {total_weight}% (should be 100%)")
    else:
        st.success(f"✅ Weights total: 100%")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Quick Stats ---
    st.markdown("### 📊 Stats")
    if st.session_state.engine:
        stats = st.session_state.engine.get_statistics()
        st.metric("📄 Total CVs", stats.get("total_cvs", 0))
        if stats.get("total_cvs", 0) > 0:
            st.metric("📈 Avg Experience", f"{stats.get('avg_experience_years', 0):.1f} yrs")
    else:
        st.metric("📄 Total CVs", 0)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear Database", use_container_width=True):
        if st.session_state.engine:
            st.session_state.engine.clear_database()
            st.session_state.processed_cvs = []
            st.session_state.search_results = []
            st.session_state.favorites = []
            st.success("✅ Database cleared!")
            st.rerun()

# ============================================================ #
#  HEADER                                                       #
# ============================================================ #
st.markdown(
    """
    <div class="fade-in">
        <h1 class="main-header">Professional CV Screening System</h1>
        <p class="sub-header">AI-Powered Semantic Search | 8 Industries | all-mpnet-base-v2</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Top Metrics Row ---
if st.session_state.engine:
    stats = st.session_state.engine.get_statistics()
    total_cvs = stats.get("total_cvs", 0)
    avg_exp   = stats.get("avg_experience_years", 0.0)
else:
    total_cvs = 0
    avg_exp   = 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f'<div class="gradient-metric"><div class="metric-label">📄 TOTAL CVs</div>'
        f'<div class="metric-value">{total_cvs}</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="gradient-metric gradient-metric-green">'
        f'<div class="metric-label">📈 AVG EXPERIENCE</div>'
        f'<div class="metric-value">{avg_exp:.1f} yrs</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="gradient-metric gradient-metric-orange">'
        f'<div class="metric-label">🏭 INDUSTRIES</div>'
        f'<div class="metric-value">{len(get_all_fields())}</div></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="gradient-metric gradient-metric-blue">'
        f'<div class="metric-label">🤖 MODEL</div>'
        f'<div class="metric-value" style="font-size:1rem;padding-top:.6rem;">mpnet-v2</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================ #
#  TABS                                                         #
# ============================================================ #
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📤 Upload CVs", "🔍 Search", "📊 Analytics", "📋 All CVs", "⭐ Favourites", "ℹ️ Help"]
)

# ──────────────────────────────────────────────────────────── #
#  TAB 1 – UPLOAD                                              #
# ──────────────────────────────────────────────────────────── #
with tab1:
    st.markdown("### 📤 Upload Candidate CVs")

    col_info, col_count = st.columns([2, 1])
    with col_info:
        st.markdown(
            """
            <div class="info-box">
                <strong>⚡ Quick Info:</strong><br>
                • Supported formats: PDF, DOCX, TXT<br>
                • Embedding model: all-mpnet-base-v2 (768 D)<br>
                • Batch upload supported – drop multiple files at once
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_count:
        st.markdown(
            f"""
            <div class="modern-card" style="text-align:center;">
                <div style="font-size:2rem;">📁</div>
                <div style="font-size:1.5rem;font-weight:bold;color:white;">{total_cvs}</div>
                <div style="color:#a0a0a0;">CVs in Database</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    uploaded_files = st.file_uploader(
        "Drop CV files here or click to browse",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        ci1, ci2, ci3 = st.columns(3)
        with ci1:
            st.info(f"📄 Files selected: {len(uploaded_files)}")
        with ci2:
            total_mb = sum(f.size for f in uploaded_files) / (1024 * 1024)
            st.info(f"💾 Total size: {total_mb:.2f} MB")
        with ci3:
            fmts = {f.name.rsplit(".", 1)[-1].upper() for f in uploaded_files}
            st.info(f"📑 Formats: {', '.join(fmts)}")

        if st.button("🚀 Process CVs", use_container_width=True):
            if not st.session_state.engine:
                st.error("⚠️ Engine not initialised – check your installation.")
            else:
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                processor = AdvancedCVProcessor(field=selected_field)
                os.makedirs("data/cvs", exist_ok=True)

                processed_count = 0
                errors: list = []

                for idx, uploaded_file in enumerate(uploaded_files):
                    status_placeholder.text(
                        f"Processing {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}"
                    )
                    try:
                        file_path = os.path.join("data/cvs", uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        cv_data = processor.process(
                            file_path, uploaded_file.name, field=selected_field
                        )
                        st.session_state.engine.add_cv(cv_data, field=selected_field)
                        st.session_state.processed_cvs.append(cv_data)
                        processed_count += 1

                    except Exception as e:
                        errors.append(f"{uploaded_file.name}: {e}")

                    progress_bar.progress((idx + 1) / len(uploaded_files))

                status_placeholder.empty()
                progress_bar.empty()

                if processed_count:
                    st.success(f"✅ Successfully processed {processed_count} CV(s)!")
                    st.balloons()
                    st.rerun()
                if errors:
                    with st.expander(f"❌ {len(errors)} file(s) failed"):
                        for err in errors:
                            st.error(err)

# ──────────────────────────────────────────────────────────── #
#  TAB 2 – SEARCH                                              #
# ──────────────────────────────────────────────────────────── #
with tab2:
    st.markdown("### 🔍 Search for Candidates")

    if total_cvs == 0:
        st.warning("⚠️ No CVs in database. Please upload CVs first (Tab 1).")
    else:
        col_q, col_opts = st.columns([3, 1])
        with col_q:
            query = st.text_area(
                "Job Description / Search Query",
                placeholder="e.g. Senior Python developer with 5+ years in Machine Learning and AWS",
                height=110,
            )
        with col_opts:
            top_k       = st.number_input("Max results", 1, 30, 5)
            use_rerank  = st.checkbox("Use re-ranking", value=True)
            min_score   = st.slider("Min match %", 0, 100, 0, 5)

        with st.expander("💡 Example queries"):
            ex = {
                "Software Engineering": (
                    "Senior Python developer with machine learning and AWS experience\n"
                    "Full-stack engineer with React, Node.js, 3–5 years\n"
                    "DevOps engineer with Kubernetes and CI/CD pipelines"
                ),
                "Pharmacy": (
                    "Clinical pharmacist with oncology experience\n"
                    "Licensed pharmacist with MTM certification\n"
                    "Pharmacy manager with retail background"
                ),
                "Teaching & Education": (
                    "Experienced maths teacher with curriculum development skills\n"
                    "ESL certified teacher with classroom management experience"
                ),
            }
            st.markdown(ex.get(selected_field, "Senior specialist with 5+ years experience"))

        if st.button("🎯 Search Candidates", use_container_width=True):
            if not query.strip():
                st.error("❌ Please enter a search query.")
            elif not st.session_state.engine:
                st.error("⚠️ Engine not initialised.")
            else:
                with st.spinner("🔍 Searching and ranking candidates…"):
                    results = st.session_state.engine.search_with_weights(
                        query=query,
                        field=selected_field,
                        weights=weights,
                        top_k=top_k,
                        use_reranking=use_rerank,
                    )

                # Filter by minimum score
                results = [r for r in results if clamp_score(r.get("final_score", 0)) >= min_score]
                st.session_state.search_results = results

                if results:
                    st.success(f"✅ Found {len(results)} matching candidate(s)!")

                    # Score bar chart
                    if len(results) > 1:
                        scores_pct = [clamp_score(r["final_score"]) for r in results]
                        fig = px.bar(
                            x=[r["name"] for r in results],
                            y=scores_pct,
                            title="Candidate Match Scores (%)",
                            labels={"x": "Candidate", "y": "Score (%)"},
                            color=scores_pct,
                            color_continuous_scale="RdYlGn",
                            template="plotly_dark",
                        )
                        fig.update_layout(showlegend=False, height=320, coloraxis_showscale=False)
                        st.plotly_chart(fig, use_container_width=True)

                    # Export button
                    df_results = cvs_to_dataframe(results)
                    csv_data = df_results.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "📥 Export Results (CSV)",
                        data=csv_data,
                        file_name=f"search_results_{datetime.now():%Y%m%d_%H%M%S}.csv",
                        mime="text/csv",
                    )

                    # Candidate cards
                    for idx, cand in enumerate(results, 1):
                        score_pct = clamp_score(cand["final_score"])
                        emoji = get_score_emoji(score_pct)

                        with st.expander(
                            f"{emoji} #{idx} – {cand['name']}  |  Match: {score_pct:.1f}%",
                            expanded=(idx == 1),
                        ):
                            m1, m2, m3, m4 = st.columns(4)
                            with m1:
                                st.metric("💼 Experience", f"{cand['years_of_experience']:.0f} yrs")
                            with m2:
                                st.metric("🎓 Education", cand.get("education_level", "N/A"))
                            with m3:
                                st.metric("🔧 Skills", len(cand.get("skills", [])))
                            with m4:
                                st.metric("📊 Score", f"{score_pct:.1f}%")

                            st.markdown("---")

                            # Score breakdown radar (component scores)
                            comp = cand.get("component_scores", {})
                            if comp:
                                comp_names  = list(comp.keys())
                                comp_values = [round(v * 100, 1) for v in comp.values()]
                                fig_radar = go.Figure(
                                    go.Scatterpolar(
                                        r=comp_values,
                                        theta=comp_names,
                                        fill="toself",
                                        line_color="#667eea",
                                    )
                                )
                                fig_radar.update_layout(
                                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                                    showlegend=False,
                                    height=280,
                                    template="plotly_dark",
                                    margin=dict(l=30, r=30, t=30, b=30),
                                )
                                st.plotly_chart(fig_radar, use_container_width=True)

                            st.markdown("**🎯 Why this candidate matches:**")
                            st.info(cand.get("match_reason", "Strong overall match"))

                            # Contact info
                            ci1, ci2, ci3 = st.columns(3)
                            with ci1:
                                st.caption(f"📧 {cand.get('email', 'N/A')}")
                            with ci2:
                                st.caption(f"📍 {cand.get('location', 'N/A')}")
                            with ci3:
                                st.caption(f"🔗 {cand.get('linkedin', 'N/A')}")

                            # Skills chips
                            if cand.get("skills"):
                                st.markdown("**🔧 Skills:**")
                                st.caption("  |  ".join(cand["skills"][:15]))

                            # Favourite button
                            fav_key = f"fav_{cand['filename']}_{idx}"
                            if st.button("⭐ Add to Favourites", key=fav_key):
                                already = any(
                                    f.get("filename") == cand.get("filename")
                                    for f in st.session_state.favorites
                                )
                                if not already:
                                    st.session_state.favorites.append(cand)
                                    st.success("Added to favourites!")
                                else:
                                    st.info("Already in favourites.")
                else:
                    st.info("ℹ️ No candidates matched. Try a different query or lower the minimum score.")
        elif not st.session_state.get("search_results"):
            st.info("👆 Enter a job description above and click **Search Candidates**")

# ──────────────────────────────────────────────────────────── #
#  TAB 3 – ANALYTICS                                           #
# ──────────────────────────────────────────────────────────── #
with tab3:
    st.markdown("### 📊 Analytics Dashboard")

    if total_cvs == 0:
        st.info("📊 Upload CVs to see analytics and insights.")
    elif st.session_state.engine:
        stats = st.session_state.engine.get_statistics()

        # Overview
        oa1, oa2, oa3 = st.columns(3)
        with oa1:
            st.metric("Total CVs", stats.get("total_cvs", 0))
        with oa2:
            st.metric("Avg Experience", f"{stats.get('avg_experience_years', 0):.1f} yrs")
        with oa3:
            st.metric("Industries", len(stats.get("by_field", {})))

        st.markdown("---")

        row1, row2 = st.columns(2)

        # CVs by Field
        with row1:
            if stats.get("by_field"):
                fig_field = px.pie(
                    names=list(stats["by_field"].keys()),
                    values=list(stats["by_field"].values()),
                    title="CVs by Industry",
                    template="plotly_dark",
                    hole=0.4,
                )
                st.plotly_chart(fig_field, use_container_width=True)

        # CVs by Experience Level
        with row2:
            if stats.get("by_experience_level"):
                fig_exp = px.bar(
                    x=list(stats["by_experience_level"].keys()),
                    y=list(stats["by_experience_level"].values()),
                    title="CVs by Experience Level",
                    template="plotly_dark",
                    color=list(stats["by_experience_level"].values()),
                    color_continuous_scale="Viridis",
                )
                fig_exp.update_layout(showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_exp, use_container_width=True)

        # Top Skills
        st.subheader("🔥 Top Skills Across All CVs")
        all_cvs_global = st.session_state.engine.get_all_cvs()
        all_skills = []
        for cv in all_cvs_global:
            all_skills.extend(cv.get("skills", []))

        if all_skills:
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(20)
            fig_skills = px.bar(
                x=[s[0] for s in top_skills],
                y=[s[1] for s in top_skills],
                labels={"x": "Skill", "y": "Count"},
                title="Most Common Skills",
                color=[s[1] for s in top_skills],
                color_continuous_scale="Viridis",
                template="plotly_dark",
            )
            fig_skills.update_xaxes(tickangle=-40)
            fig_skills.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_skills, use_container_width=True)

        # Education breakdown
        if stats.get("by_education_level"):
            fig_edu = px.pie(
                names=list(stats["by_education_level"].keys()),
                values=list(stats["by_education_level"].values()),
                title="CVs by Education Level",
                template="plotly_dark",
            )
            st.plotly_chart(fig_edu, use_container_width=True)

# ──────────────────────────────────────────────────────────── #
#  TAB 4 – ALL CVS                                             #
# ──────────────────────────────────────────────────────────── #
with tab4:
    st.markdown("### 📋 All CVs in Database")

    if total_cvs == 0:
        st.info("📋 No CVs yet – upload some in Tab 1.")
    elif st.session_state.engine:
        filter_col, sort_col = st.columns(2)
        with filter_col:
            filter_field = st.selectbox(
                "Filter by industry",
                ["All"] + get_all_fields(),
                key="tab4_filter",
            )
        with sort_col:
            sort_by = st.selectbox(
                "Sort by",
                ["Name (A–Z)", "Experience (High–Low)", "Education"],
                key="tab4_sort",
            )

        field_arg = None if filter_field == "All" else filter_field
        all_cvs = st.session_state.engine.get_all_cvs(field=field_arg)

        # Sort
        if sort_by == "Experience (High–Low)":
            all_cvs.sort(key=lambda x: x.get("years_of_experience", 0), reverse=True)
        elif sort_by == "Name (A–Z)":
            all_cvs.sort(key=lambda x: x.get("name", "").lower())
        elif sort_by == "Education":
            edu_order = {"PhD": 0, "Master's": 1, "Bachelor's": 2, "Associate/Diploma": 3, "Not specified": 4}
            all_cvs.sort(key=lambda x: edu_order.get(x.get("education_level", "Not specified"), 5))

        st.caption(f"Showing {len(all_cvs)} CV(s)")

        # Export all
        if all_cvs:
            df_all = cvs_to_dataframe(all_cvs)
            csv_all = df_all.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export All CVs (CSV)",
                data=csv_all,
                file_name=f"all_cvs_{datetime.now():%Y%m%d_%H%M%S}.csv",
                mime="text/csv",
            )

        for idx, cv in enumerate(all_cvs, 1):
            with st.expander(
                f"📄 {idx}. {cv['name']}  |  {cv.get('experience_level', 'N/A')}"
                f"  |  {cv.get('years_of_experience', 0):.0f} yrs exp"
            ):
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**📧 Email:** {cv.get('email', 'N/A')}")
                    st.markdown(f"**📍 Location:** {cv.get('location', 'N/A')}")
                    st.markdown(f"**🎓 Education:** {cv.get('education_level', 'N/A')}")
                    st.markdown(f"**🏭 Field:** {cv.get('field', 'N/A')}")
                with c2:
                    st.markdown("**🔧 Skills:**")
                    st.caption(", ".join(cv.get("skills", [])[:15]) or "None listed")
                    if cv.get("certifications"):
                        st.markdown("**📜 Certifications:**")
                        st.caption(", ".join(cv["certifications"][:5]))

# ──────────────────────────────────────────────────────────── #
#  TAB 5 – FAVOURITES                                          #
# ──────────────────────────────────────────────────────────── #
with tab5:
    st.markdown("### ⭐ Favourite Candidates")

    favs = st.session_state.get("favorites", [])
    if not favs:
        st.info("⭐ No favourites yet – click the star button on search results.")
    else:
        # Export
        df_favs = cvs_to_dataframe(favs)
        csv_favs = df_favs.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export Favourites (CSV)",
            data=csv_favs,
            file_name=f"favourites_{datetime.now():%Y%m%d_%H%M%S}.csv",
            mime="text/csv",
        )

        for idx, fav in enumerate(favs, 1):
            score_pct = clamp_score(fav.get("final_score", 0))
            with st.expander(f"⭐ #{idx} – {fav.get('name', 'Candidate')}  |  {score_pct:.1f}% match"):
                f1, f2 = st.columns(2)
                with f1:
                    st.markdown(f"**💼 Experience:** {fav.get('years_of_experience', 0):.0f} years")
                    st.markdown(f"**🎓 Education:** {fav.get('education_level', 'N/A')}")
                    st.markdown(f"**📧 Email:** {fav.get('email', 'N/A')}")
                with f2:
                    st.markdown(f"**🔧 Skills ({len(fav.get('skills', []))}):**")
                    st.caption(", ".join(fav.get("skills", [])[:10]))
                st.markdown("**Match Reason:**")
                st.info(fav.get("match_reason", "N/A"))

                if st.button("🗑️ Remove", key=f"remove_fav_{idx}"):
                    st.session_state.favorites.remove(fav)
                    st.rerun()

# ──────────────────────────────────────────────────────────── #
#  TAB 6 – HELP                                                #
# ──────────────────────────────────────────────────────────── #
with tab6:
    st.markdown("### ℹ️ Help & Information")

    h1, h2 = st.columns(2)
    with h1:
        st.markdown(
            """
            <div class="modern-card">
                <h4 style="color:white;">🚀 Quick Start</h4>
                <ol style="color:#e0e0e0;">
                    <li>Select your industry from the sidebar</li>
                    <li>Upload CVs (PDF, DOCX, TXT)</li>
                    <li>Adjust scoring weights to match your priorities</li>
                    <li>Enter a job description in Search</li>
                    <li>Export results as CSV</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="modern-card" style="margin-top:1rem;">
                <h4 style="color:white;">🎯 Key Features</h4>
                <ul style="color:#e0e0e0;">
                    <li>🔍 Semantic search (768-D embeddings)</li>
                    <li>🔄 Cross-encoder re-ranking</li>
                    <li>📊 Real-time analytics dashboard</li>
                    <li>⭐ Favourites with export</li>
                    <li>🎛️ Per-field dynamic weight defaults</li>
                    <li>📥 CSV export for all views</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with h2:
        st.markdown(
            """
            <div class="modern-card">
                <h4 style="color:white;">🔬 How It Works</h4>
                <p style="color:#e0e0e0;">
                    Each CV is converted to a 768-dimensional vector using
                    <strong>all-mpnet-base-v2</strong>. Searches embed your
                    job description the same way, then find the closest
                    vectors in ChromaDB (cosine similarity).
                </p>
                <p style="color:#e0e0e0;">
                    A weighted scoring layer boosts candidates based on
                    skills, experience, education, projects, and
                    certifications. An optional cross-encoder re-ranker
                    (<em>ms-marco-MiniLM-L-6-v2</em>) adds a second pass
                    of relevance scoring.
                </p>
                <code style="color:#e0e0e0;">
                    CV → Embed → ChromaDB → Weighted Score → Re-rank → Results
                </code>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="modern-card" style="margin-top:1rem;">
                <h4 style="color:white;">💡 Tips for Better Results</h4>
                <ul style="color:#e0e0e0;">
                    <li>Use natural language job descriptions, not keyword lists</li>
                    <li>Mention required years of experience explicitly</li>
                    <li>Enable re-ranking for the most accurate ordering</li>
                    <li>Adjust weights based on role seniority</li>
                    <li>Use the minimum score filter to remove weak matches</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="custom-divider"></div>
        <div style="text-align:center;padding:1rem;">
            <h4 style="color:white;">📚 Technology Stack</h4>
            <p style="color:#a0a0a0;">
                Streamlit · Sentence-Transformers · ChromaDB · Plotly · PyPDF2 · python-docx · Pandas
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================ #
#  FOOTER                                                       #
# ============================================================ #
st.markdown(
    """
    <div class="footer">
        <p>CV Screening Pro v2.1 · AI-Powered Recruitment Platform · © 2024</p>
        <p style="font-size:.7rem;">
            Embedding: all-mpnet-base-v2 (768 D) · Re-ranker: ms-marco-MiniLM-L-6-v2 · DB: ChromaDB (cosine)
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
