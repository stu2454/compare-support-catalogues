import streamlit as st
import os

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="NDIS Support Catalogue Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Determine the correct pages directory path
# This handles both local and Docker environments
if os.path.exists("pages"):
    pages_dir = "pages"
elif os.path.exists("/app/pages"):
    pages_dir = "/app/pages"
else:
    pages_dir = "pages"  # default

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("**Select a page:**")
    st.markdown("")
    
    # Use st.page_link for proper navigation
    try:
        st.page_link("streamlit_app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Compare_Versions.py", label="Compare Versions", icon="📊")
        st.page_link("pages/2_JSON_Explainer.py", label="JSON Explainer", icon="📖")
    except Exception as e:
        # Fallback if page_link doesn't work
        st.error(f"Navigation error: {e}")
        st.info("Please use the page selector that should appear above this section.")
    
    st.markdown("---")
    
    # Debug info to help troubleshoot
    with st.expander("🔧 Troubleshooting Info"):
        st.write("**Current working directory:**", os.getcwd())
        st.write("**Pages directory exists:**", os.path.exists("pages"))
        if os.path.exists("pages"):
            st.write("**Files in pages/:**", os.listdir("pages"))
        else:
            st.error("❌ pages/ directory not found!")
            st.write("Please ensure you're running: `streamlit run streamlit_app.py`")


# Load CSS
with open("ndis_theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🏛️ NDIS Support Catalogue Comparison Tool")
st.markdown("**Markets Delivery · National Disability Insurance Agency**")

st.markdown("---")

# Introduction
st.markdown("""
Welcome to the **NDIS Support Catalogue Comparison Tool** – a digital-first prototype for modernizing 
how we work with NDIS pricing information.

This tool helps NDIA staff, analysts, and stakeholders:
- Transform static Excel catalogues into structured, machine-readable JSON
- Compare catalogue versions with detailed change detection
- Understand the business value of digital-first pricing artefacts
""")

st.markdown("---")

# Navigation cards
st.subheader("🧭 What You Can Do")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="nav-card">
        <h3>📊 Compare Versions</h3>
        <p><strong>Main workflow</strong></p>
        <p>Upload two Support Catalogue Excel files (OLD vs NEW) and get detailed change detection:</p>
        <ul>
            <li>Added, removed, or moved items</li>
            <li>Field-level modifications</li>
            <li>Downloadable JSON outputs</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <h3>📖 JSON Conversion Explainer</h3>
        <p><strong>Why this matters</strong></p>
        <p>Plain English explainer covering:</p>
        <ul>
            <li>Why static documents are insufficient</li>
            <li>What JSON is and why it matters</li>
            <li>How this enables better stewardship</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 **To access these pages:** Look in the left sidebar under 'Navigation' and click the page links")

st.markdown("---")

# Getting started
st.subheader("🚀 Getting Started")

st.markdown("""
**Look in the left sidebar** for the **🧭 Navigation** section with clickable page links:

1. **Start with the Explainer** (recommended for first-time users)
   - Click **"📖 JSON Explainer"** in the sidebar
   - Learn why we're moving to structured data

2. **Try the comparison workflow**
   - Click **"📊 Compare Versions"** in the sidebar
   - Upload two catalogue Excel files
   - Map sheets and explore the changes

3. **Download JSON outputs**
   - Each comparison generates downloadable JSON files
   - Use these for validation, dashboards, or API integration
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p><strong>NDIS Support Catalogue Comparison Tool</strong> · Markets Delivery</p>
    <p>Built for internal NDIA use · Prototype for digital transformation</p>
</div>
""", unsafe_allow_html=True)