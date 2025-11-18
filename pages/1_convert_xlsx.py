import json
import sys
import tempfile
from pathlib import Path

import streamlit as st

# Ensure local imports work in Docker
sys.path.append("/app")
from xlsx_to_json import parse_xlsx_to_json


# ---------------------------------------------------------
# Theme loader
# ---------------------------------------------------------
def load_ndis_theme():
    candidates = [
        Path(__file__).resolve().parents[1] / "ndis_theme.css",
        Path("/app/ndis_theme.css"),
    ]
    for c in candidates:
        if c.exists():
            st.markdown(f"<style>{c.read_text()}</style>", unsafe_allow_html=True)
            return
    st.error("❌ ndis_theme.css not found. Check Dockerfile and project root.")

load_ndis_theme()

st.set_page_config(
    page_title="Convert Support Catalogue",
    page_icon="📂",
    layout="wide",
)

# ---------------------------------------------------------
# Title / intro
# ---------------------------------------------------------
st.markdown("<div class='nids-content'>", unsafe_allow_html=True)

st.markdown("<div class='nids-main-title'>Convert Support Catalogue XLSX → JSON</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='nids-subtitle'>Upload the official Excel workbook and generate a structured JSON catalogue for downstream tools.</div>",
    unsafe_allow_html=True,
)

if "catalogue_json" not in st.session_state:
    st.session_state.catalogue_json = None
    st.session_state.catalogue_meta = None
    st.session_state.catalogue_name = None

# ---------------------------------------------------------
# Layout: responsive grid with two cards
# ---------------------------------------------------------
st.markdown('<div class="nids-grid">', unsafe_allow_html=True)

# LEFT CARD: upload + options + convert
st.markdown('<div class="col-span-5 nids-card">', unsafe_allow_html=True)
st.markdown("<div class='nids-section-header'>📂 Upload & Convert</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload NDIS Support Catalogue XLSX",
    type=["xlsx"],
    help="Use the official NDIS Support Catalogue Excel file.",
)

sheet_name = st.text_input(
    "Sheet name containing current support items",
    value="Current Support Items",
    help="Update this if the tab is named differently.",
)

convert_button = st.button("Convert to JSON", type="primary")

if convert_button:
    if not uploaded_file:
        st.error("Please upload an Excel file first.")
    else:
        with st.spinner("Parsing XLSX and building JSON catalogue…"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name

            try:
                catalogue = parse_xlsx_to_json(tmp_path, sheet_name=sheet_name)
            except Exception as e:
                st.error(f"Error while parsing workbook: {e}")
            else:
                st.session_state.catalogue_json = catalogue
                st.session_state.catalogue_meta = catalogue.get("metadata", {})
                st.session_state.catalogue_name = uploaded_file.name
                st.success("Conversion complete. Preview and download are available in the panel on the right.")

st.markdown("</div>", unsafe_allow_html=True)  # end left card

# RIGHT CARD: preview + metadata + download
st.markdown('<div class="col-span-7 nids-card">', unsafe_allow_html=True)
st.markdown("<div class='nids-section-header'>📊 Preview & Download</div>", unsafe_allow_html=True)

if st.session_state.catalogue_json is None:
    st.info("Once you convert a catalogue, a summary and data preview will appear here.")
else:
    meta = st.session_state.catalogue_meta or {}
    items = st.session_state.catalogue_json.get("support_items", [])

    st.write(
        f"**Source file:** `{meta.get('source_file', st.session_state.catalogue_name)}`  "
        f"• **Version:** `{meta.get('catalogue_version', 'unknown')}`  "
        f"• **Total items:** `{meta.get('total_items', len(items))}`  "
        f"• **Conversion errors:** `{meta.get('conversion_errors', 0)}`"
    )

    if items:
        preview_rows = []
        for item in items[:25]:
            preview_rows.append({
                "Support item number": item.get("support_item_number"),
                "Name": item.get("support_item_name"),
                "Category": item.get("support_category_name"),
                "Unit": item.get("unit"),
                "Quote": "Yes" if item.get("quote") else "No",
            })
        st.write("Preview of first 25 support items:")
        st.dataframe(preview_rows, use_container_width=True)
    else:
        st.warning("No support items found in parsed data.")

    json_bytes = json.dumps(
        st.session_state.catalogue_json,
        indent=2,
        ensure_ascii=False
    ).encode("utf-8")

    default_name = (st.session_state.catalogue_name or "support-catalogue").replace(".xlsx", "") + ".json"

    st.download_button(
        "⬇️ Download JSON catalogue",
        data=json_bytes,
        file_name=default_name,
        mime="application/json",
    )

st.markdown("</div>", unsafe_allow_html=True)  # end right card
st.markdown("</div>", unsafe_allow_html=True)  # end grid
st.markdown("</div>", unsafe_allow_html=True)  # end nids-content

