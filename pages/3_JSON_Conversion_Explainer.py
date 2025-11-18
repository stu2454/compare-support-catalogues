import streamlit as st

# ---------------------------------------------------------
# Wide layout
# ---------------------------------------------------------
st.set_page_config(layout="wide")

# ---------------------------------
# NDIA heading component (fixed)
# ---------------------------------
def section_heading(text):
    st.markdown(
        f"<div class='section-header'>{text}</div>",
        unsafe_allow_html=True
    )

# ---------------------------------
# NDIA-styled framed image component (Streamlit-safe)
# ---------------------------------
def framed_image(img_path, max_width=1000):
    # outer card wrapper
    st.markdown(
        f"""
        <div style="
            border: 1px solid #DDDDDD;
            padding: 14px;
            border-radius: 12px;
            margin: 1.5rem 0;
            background-color: #ffffff;
            max-width: {max_width}px;
        ">
        """,
        unsafe_allow_html=True,
    )
    # image served via Streamlit
    st.image(img_path, use_container_width=True)
    # close card wrapper
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("Why We Convert NDIA Pricing Artefacts into JSON")
st.write("A comprehensive, plain-English explainer for NDIA colleagues")

# =========================================================
# INTRODUCTION
# =========================================================

st.markdown(
    """
<div class="card">
<div class="pill">Introduction</div>
<h3>Why this explainer exists</h3>

<p>
The NDIA’s most important pricing artefacts — the Support Catalogue,
the Pricing Arrangements and Price Limits (PAPL), the Code Guides,
and the Operational Guidelines — are all stored today as 
<strong>static documents</strong>. Some are Excel files, others
Word documents, PDFs, or HTML pages.
</p>

<p>
These formats work well for humans. But they are <strong>not designed 
for digital tools</strong>. If the NDIA wants to move toward 
Digital-First Pricing Artefacts, modern search, automated validation, 
version comparison, dashboards and AI-supported experiences, we must
convert these documents into <strong>structured, machine-readable 
data</strong>.
</p>

<p>
The most practical format for this is <strong>JSON</strong>.
</p>

<p>This page explains in plain English:</p>

<ul>
<li>why static documents are not enough</li>
<li>why JSON is so powerful</li>
<li>how the conversion process works</li>
<li>what this unlocks for the Agency</li>
</ul>

</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# SECTION 1 – WHY STATIC DOCUMENTS ARE NOT ENOUGH
# =========================================================

section_heading("1. Why static documents (Excel, Word, PDF, HTML) are not enough")

with st.expander("1.1 Documents are for people, not machines"):
    st.markdown("""
Static documents were never designed to be the foundation for digital services.
They are great for human reading but unreliable for systems that require 
precision and consistency.

Humans can interpret layout, tables, crossed-out text, footnotes and structure.
Machines cannot.

Behind the scenes, spreadsheets contain:
- merged cells  
- formatting  
- hidden columns  
- inconsistent entries  

PDFs and Word files contain:
- tables inside paragraphs  
- ambiguous formatting  
- cross-references that break  
    """)

with st.expander("1.2 Every release is slightly different"):
    st.markdown("""
Even tiny changes break automated processing:
- column names shift  
- tables reorder  
- wording changes  
- new fields appear  

Humans adjust. Machines cannot unless data is structured.
    """)

with st.expander("1.3 Every NDIA team reinterprets the documents differently"):
    st.markdown("""
Different teams extract meaning differently:
- ACTU  
- Markets  
- ICT  
- Analytics  
- Planners and providers  

This leads to duplicated effort, inconsistent interpretations and governance risk.
    """)

with st.expander("1.4 Real-world metaphors"):
    st.markdown("""
- Document = printed recipe  
- JSON = ingredients measured and labelled  

- Document = photo of a map  
- JSON = GPS coordinates  
    """)

# =========================================================
# SECTION 2 – WHAT JSON IS
# =========================================================

section_heading("2. What JSON is (plain English only)")

with st.expander("A simple, predictable structure"):
    st.markdown("""
JSON is a clean, labelled format for storing data.

Example:

```
"item_number": "05_123456",
"support_name": "Specialised shower chair",
"price_limit_nsw": 239.50
```

Machines read it instantly.  
It is unambiguous and consistent across releases.  
    """)

with st.expander("Metaphors that make JSON obvious"):
    st.markdown("""
- JSON is Lego blocks — uniform pieces that snap together  
- JSON is a library index — clear categories, no guesswork  
    """)

# ----------------------------------------------------
# INSERT IMAGE: WHY JSON MATTERS
# ----------------------------------------------------
st.subheader("Visual: Why JSON Matters")
framed_image("assets/why_JSON_matters.png")

# =========================================================
# SECTION 3 – WHY CONVERSION IS NECESSARY
# =========================================================

section_heading("3. Why conversion to JSON is necessary for Digital-First Pricing Artefacts")

with st.expander("3.1 Compare versions instantly"):
    st.markdown("""
JSON enables instant tracking of:
- added items  
- removed items  
- price changes  
- claim type changes  
    """)

with st.expander("3.2 Automate validation"):
    st.markdown("""
JSON allows automated rule-checking:
- missing values  
- incorrect formats  
- cap checks  
- state mismatches  
    """)

with st.expander("3.3 Improve interfaces for planners, providers and policy teams"):
    st.markdown("""
JSON enables:
- search  
- filters  
- item comparison  
- context-aware guidance  
    """)

with st.expander("3.4 Strengthen market stewardship"):
    st.markdown("""
Structured data enables:
- price movement tracking  
- anomaly detection  
- provider benchmarking  
- forecasting  
    """)

with st.expander("3.5 Enable safe LLM-based tools"):
    st.markdown("""
LLMs hallucinate far less when reading structured JSON instead of PDFs or Word files.
    """)

with st.expander("3.6 Provide a consistent, auditable source of truth"):
    st.markdown("""
JSON ensures:
- traceability  
- reproducibility  
- governance  
    """)

# ----------------------------------------------------
# INSERT IMAGE: STATIC → STRUCTURE → STEWARDSHIP
# ----------------------------------------------------
st.subheader("Visual: Static → Structure → Stewardship")
framed_image("assets/static_structured_stewardship.png")

# =========================================================
# SECTION 4 – HOW THE CONVERSION WORKS
# =========================================================

section_heading("4. How the conversion process works (plain English)")

with st.expander("Step-by-step process"):
    st.markdown("""
**Step 1 — Upload**  
Excel, Word, PDF or HTML provided.

**Step 2 — Parse**  
System reads cells, tables, headings.

**Step 3 — Extract meaning**  
Headings → JSON fields.

**Step 4 — Standardise**  
Dates, Yes/No, null values, prices.

**Step 5 — Structure**  
Apply consistent schema.

**Step 6 — Output JSON**  
Ready for version comparison, dashboards, AI tools, planning tools.
    """)

with st.expander("Why this matters"):
    st.markdown("""
JSON conversion is:
- deterministic  
- repeatable  
- auditable  
- governed  
    """)

# -----------------------------------------------------------
# INSERT IMAGE: COMPLETE PIPELINE
# -----------------------------------------------------------
st.subheader("Visual: From Static Artefacts to Digital-First Tools")
framed_image("assets/transformation_of_artefacts.png")

# =========================================================
# END – RETURN LINK
# =========================================================

st.divider()
st.page_link("pages/1_convert_xlsx.py", label="← Back to XLSX Conversion Tool")
