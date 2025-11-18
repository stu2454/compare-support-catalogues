import streamlit as st
from pathlib import Path

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="NDIS Support Catalogue Tools",
    page_icon="📚",
    layout="wide",
)

# ---------------------------------------------------------
# Bullet-proof NDIS theme loader
# ---------------------------------------------------------
def load_ndis_theme():
    """
    Load ndis_theme.css and inject as a <style> block.
    This prevents the CSS being rendered as visible text.
    """
    candidates = [
        Path(__file__).resolve().parent / "ndis_theme.css",
        Path(__file__).resolve().parent.parent / "ndis_theme.css",
        Path("/app/ndis_theme.css"),
    ]
    for c in candidates:
        if c.exists():
            css = c.read_text()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
            return
    st.error("❌ Could not find ndis_theme.css. Ensure it is in the project root and Docker copies it.")

load_ndis_theme()

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown("<div class='nids-content'>", unsafe_allow_html=True)

st.markdown(
    "<div class='nids-main-title'>NDIS Digital-First Pricing Artefacts</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='nids-subtitle'>Internal tooling to convert and compare Support Catalogue versions.</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Responsive grid with two cards
#   IMPORTANT: the HTML string starts directly with '<div'
#   so Markdown treats it as HTML, not a code block.
# ---------------------------------------------------------
home_grid_html = """<div class="nids-grid">

  <div class="col-span-6 nids-card">
    <div class="nids-pill">Step 1</div>
    <div class="nids-section-header">📂 Convert XLSX → JSON</div>
    <p>
      Use the <strong>Convert XLSX → JSON</strong> page to:
    </p>
    <ul>
      <li>Upload the official NDIS Support Catalogue Excel file</li>
      <li>Convert it into structured JSON</li>
      <li>Normalise booleans, prices and dates</li>
      <li>Expose per-state price limits</li>
      <li>Flag claim types and quote requirements</li>
      <li>Download JSON for analysis or comparison</li>
    </ul>
  </div>

  <div class="col-span-6 nids-card">
    <div class="nids-pill">Step 2</div>
    <div class="nids-section-header">🔍 Compare Catalogue Versions</div>
    <p>
      Use the <strong>Compare Versions</strong> page to:
    </p>
    <ul>
      <li>Upload an <strong>old</strong> and <strong>new</strong> Support Catalogue JSON</li>
      <li>Identify items added, removed or modified</li>
      <li>See price changes by state, with percentage change</li>
      <li>Detect changes in claim types</li>
      <li>Generate Markdown and PDF reports for briefings</li>
    </ul>
  </div>

</div>"""

st.markdown(home_grid_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer / hint
# ---------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    """
    Use the left-hand navigation to switch between tools.  
    This platform demonstrates why **structured JSON** dramatically improves clarity
    compared with static PDFs when analysing changes to pricing artefacts.
    """
)

st.markdown("</div>", unsafe_allow_html=True)  # end nids-content


