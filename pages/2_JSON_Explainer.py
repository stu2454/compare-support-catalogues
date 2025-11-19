"""
JSON Conversion Explainer

Plain English explanation of:
- Why static documents are insufficient
- What JSON is and why it matters
- How the conversion process works
- What this unlocks for NDIA
"""

import streamlit as st
import os

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="JSON Conversion Explainer",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ndis_theme.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("📖 JSON Conversion Explainer")
st.markdown("**Understanding Digital-First Pricing Artefacts**")
st.markdown("---")

# Introduction
st.markdown("""
This page explains **why** we're moving NDIS pricing information from static documents (Excel, Word, PDF) 
to structured, machine-readable formats like JSON — and **what this enables** for the NDIA, service providers, 
and participants.
""")

st.markdown("---")

# Section 1: The Problem
st.header("1. 🚨 The Problem: Static Documents Are Insufficient")

st.markdown("""
Right now, the key NDIS pricing artefacts exist as:
- **Support Catalogue**: Excel (.xlsx) files with 600+ rows
- **Pricing Arrangements and Price Limits (PAPL)**: Word/PDF documents
- **Code Guides**: Word/PDF/HTML documents
- **Operational Guidelines**: HTML pages

### Why this is problematic:

**For NDIA teams:**
- 🔍 **Hard to search**: Finding a specific support item requires manually scrolling through spreadsheets
- 🔄 **Hard to compare**: Detecting changes between versions requires manual diff'ing
- 🧮 **Hard to validate**: No automated checks for business rules or data quality
- 📊 **Hard to analyze**: Can't easily generate reports or dashboards
- 🤝 **Inconsistent interpretation**: Different teams (Markets, ACTU, ICT, Analytics) re-interpret the same data differently

**For service providers & software vendors:**
- 🔌 **No API access**: Can't programmatically query pricing information
- 💾 **Manual data entry**: Must re-key information into their systems
- ⚠️ **Version drift**: Hard to know which version is current
- 🐛 **Error-prone**: Manual processes introduce mistakes

**For participants:**
- ❓ **Opacity**: Hard to understand what supports are available
- 💰 **Price confusion**: Unclear what services should cost
""")

st.markdown("---")

# Section 2: What is JSON?
st.header("2. 📦 What is JSON? (In Plain English)")

st.markdown("""
**JSON** stands for **JavaScript Object Notation**, but you don't need to know JavaScript to understand it.

Think of JSON as a way to structure information so that:
1. **Humans can read it** (it looks like indented text with labels)
2. **Computers can process it** (it follows strict rules)
3. **It's unambiguous** (there's only one way to interpret each piece of data)

### Example: A Support Item in Excel vs JSON

**In Excel (human-readable but not machine-friendly):**

| Item Number | Support Name | Unit | Price Limit NSW | Price Limit VIC |
|-------------|--------------|------|-----------------|-----------------|
| 05_123456 | Specialised shower chair | Each | 239.5 | 240.0 |

**In JSON (both human-readable AND machine-friendly):**

```json
{
  "item_number": "05_123456",
  "support_name": "Specialised shower chair",
  "unit": "Each",
  "price_limit_nsw": 239.5,
  "price_limit_vic": 240.0,
  "effective_from": "2024-07-01",
  "effective_to": null
}
```

### Key benefits of JSON:

- ✅ **Structured**: Each field has a clear type (text, number, date, true/false)
- ✅ **Validated**: We can check that every item follows the rules
- ✅ **Queryable**: Computers can search, filter, and compare instantly
- ✅ **Versionable**: We can track what changed, when, and by whom
- ✅ **Reusable**: The same data can power websites, apps, dashboards, and reports
""")

st.markdown("---")

# Section 3: The Conversion Process
st.header("3. 🔧 How the Conversion Works")

st.markdown("""
This tool converts Excel catalogues to JSON in several steps:

### Step 1: Sheet Detection
- Analyzes the workbook and lists all sheets
- Shows row counts to help you identify Current vs Legacy sheets
- Handles different naming conventions across years

### Step 2: Column Mapping
- Automatically detects column names even when they vary
  - "Item Number" vs "Support Item Number" → maps to `item_number`
  - "NSW" vs "New South Wales" vs "NSW Price Limit" → maps to `price_limit_nsw`
- Handles extra or missing columns gracefully

### Step 3: Data Normalization
- Converts dates to YYYY-MM-DD format
- Converts "Yes"/"No" to true/false
- Converts prices to numbers
- Converts empty cells to null
- Trims whitespace and standardizes formatting

### Step 4: Validation
- Ensures every item has an item_number
- Checks data types are correct
- Flags anomalies and inconsistencies

### Step 5: Structured Output
- Generates a clean JSON file with:
  - Metadata (source file, generation date, row counts)
  - Current items array
  - Legacy items array (if present)
""")

# Diagram placeholder 1
st.markdown("---")
st.markdown("### The Transformation Process:")
st.markdown("""
<div class="image-card">
<p><em>Diagram: transformation_of_artefacts.png would appear here showing the flow from Excel → JSON → Applications</em></p>
<p style="background-color: #f0f0f0; padding: 2rem; text-align: center; border-radius: 8px;">
📊 Excel Spreadsheet → 🔄 Conversion Tool → 📦 Structured JSON → 🚀 APIs, Dashboards, Validation Tools
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Section 4: What This Unlocks
st.header("4. 🚀 What Structured Data Unlocks for NDIA")

st.markdown("""
Once pricing information is in JSON format, we can build powerful tools on top of it:

### For Markets Delivery:
- 📊 **Version comparison dashboards**: See exactly what changed between catalogue versions
- ✅ **Automated validation**: Check business rules (e.g., "all current items must have prices for all states")
- 📈 **Trend analysis**: Track price changes over time
- 🔍 **Smart search**: Find items by category, registration group, or price range
- 📝 **Impact reports**: Generate executive summaries showing what changed and why it matters

### For ACTU / Policy Teams:
- 🔬 **Business rule testing**: Ensure new catalogues comply with policy requirements
- 📋 **Audit trails**: Track the history of every support item
- 🎯 **Consistency checks**: Verify that PAPL documents align with catalogue data

### For ICT / Systems:
- 🔌 **APIs**: Expose pricing data to internal and external systems
- 🤖 **Automation**: Update pricing in downstream systems automatically
- 🛡️ **Data quality**: Catch errors before they reach production

### For Analytics:
- 📊 **Dashboards**: Build real-time views of pricing data
- 📉 **Market analysis**: Understand pricing patterns and trends
- 🎨 **Visualizations**: Create charts and graphs from structured data

### For Service Providers:
- 🔌 **API access**: Software vendors can query pricing directly
- ✅ **Validation**: Check if their claims align with current pricing
- 🔄 **Auto-updates**: Systems stay in sync with latest catalogue

### For Safe AI/LLM Tools:
- 🤖 **Reliable inputs**: LLMs can work with structured data rather than parsing documents
- ✅ **Fact-checking**: Verify AI outputs against authoritative JSON data
- 📚 **Knowledge bases**: Build AI assistants that understand NDIS pricing accurately
""")

# Diagram placeholder 2
st.markdown("---")
st.markdown("### Why JSON Matters:")
st.markdown("""
<div class="image-card">
<p><em>Diagram: why_JSON_matters.png would appear here showing the comparison between document-based and structured approaches</em></p>
<p style="background-color: #f0f0f0; padding: 2rem; text-align: center; border-radius: 8px;">
📄 Static Documents:<br>
Manual processes → Errors → Inconsistency → Limited automation
<br><br>
vs
<br><br>
📦 Structured JSON:<br>
Automated validation → Consistency → APIs → Rich applications
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Section 5: Market Stewardship
st.header("5. 🏛️ Better Market Stewardship")

st.markdown("""
Digital-first pricing artefacts are not just about technology — they're about **better governance and stewardship** of the NDIS market.

### Current state (document-based):
- 📄 Pricing information "locked" in PDFs and Excel files
- 🤷 Ambiguity about what's current vs what's historical
- ⏰ Lag time between policy decisions and system updates
- 🐛 Errors discovered too late in the process
- 🔀 Different interpretations across different systems

### Future state (structured data):
- 📦 Single source of truth for pricing information
- ✅ Validated data that follows business rules
- 🔄 Version-controlled history showing what changed and when
- 🚀 Immediate propagation of updates to all systems
- 🛡️ Proactive detection of anomalies and inconsistencies
- 🤝 Shared understanding across all NDIA teams and external stakeholders
""")

# Diagram placeholder 3
st.markdown("---")
st.markdown("### Static vs Structured Stewardship:")
st.markdown("""
<div class="image-card">
<p><em>Diagram: static_structured_stewardship.png would appear here showing governance improvements</em></p>
<p style="background-color: #f0f0f0; padding: 2rem; text-align: center; border-radius: 8px;">
📊 Old way: Manual processes → Delayed validation → Reactive fixes
<br><br>
🚀 New way: Automated validation → Proactive governance → Continuous improvement
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Section 6: This Tool
st.header("6. 🔧 About This Tool")

st.markdown("""
This **NDIS Support Catalogue Comparison Tool** is a proof-of-concept that demonstrates:

1. **Robust conversion**: Handles different Excel formats and naming conventions
2. **Smart comparison**: Detects 7 types of changes (added, removed, modified, etc.)
3. **Field-level tracking**: Shows exactly which fields changed for each item
4. **Governance support**: Flags items requiring review (e.g., removed without legacy)
5. **Professional UI**: Designed for internal NDIA use, not a toy demo

### What this proves:
- ✅ We **can** convert existing catalogues to JSON reliably
- ✅ We **can** detect and categorize changes automatically
- ✅ We **can** provide actionable insights for stakeholders
- ✅ We **can** build internal tools that feel credible and professional

### What's next:
This is a **prototype**. If validated, the next steps would be:
1. Integrate with official NDIA systems and workflows
2. Expand to other pricing artefacts (PAPL, Code Guides)
3. Build APIs and dashboards for broader use
4. Establish governance processes for maintaining structured data
5. Enable safe AI/LLM tools that work with authoritative pricing information
""")

st.markdown("---")

# Footer
st.success("""
**Ready to try it?** Navigate to **Compare Versions** in the sidebar to upload two catalogue files 
and see the conversion in action.
""")

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p><strong>JSON Conversion Explainer</strong> · Markets Delivery · NDIA</p>
    <p>Questions? Contact the digital transformation team.</p>
</div>
""", unsafe_allow_html=True)