"""
Compare Support Catalogue Versions

Main workflow:
1. Upload OLD and NEW Excel files
2. Map sheets (Current + Legacy) via tabs
3. Convert to JSON
4. Run comparison
5. Display results with expanders
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xlsx_to_json
import version_diff

# Page config
st.set_page_config(
    page_title="Compare Catalogue Versions",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS theme
css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ndis_theme.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("🔄 Compare Support Catalogue Versions")
st.markdown("Upload two catalogue Excel files and compare changes across versions")
st.markdown("---")

# Session state init
if "old_file_uploaded" not in st.session_state:
    st.session_state.old_file_uploaded = False
    st.session_state.new_file_uploaded = False
    st.session_state.old_sheets_info = None
    st.session_state.new_sheets_info = None
    st.session_state.old_current_sheet = None
    st.session_state.old_legacy_sheet = None
    st.session_state.new_current_sheet = None
    st.session_state.new_legacy_sheet = None
    st.session_state.old_json = None
    st.session_state.new_json = None
    st.session_state.comparison_results = None


# ---------------------------------------------------------
# STEP 1 — FILE UPLOAD
# ---------------------------------------------------------
st.subheader("📤 Step 1: Upload Catalogue Files")

col1, col2 = st.columns(2)

with col1:
    old_file = st.file_uploader(
        "Upload OLD Catalogue (Excel)",
        type=["xlsx"],
        key="old_upload"
    )

with col2:
    new_file = st.file_uploader(
        "Upload NEW Catalogue (Excel)",
        type=["xlsx"],
        key="new_upload"
    )

# Handle OLD upload
if old_file:
    if not st.session_state.old_file_uploaded or st.session_state.get("old_filename") != old_file.name:
        with st.spinner("Analyzing OLD catalogue sheets..."):
            temp_path = f"/tmp/old_catalogue_{datetime.now().timestamp()}.xlsx"
            with open(temp_path, "wb") as f:
                f.write(old_file.getvalue())

            st.session_state.old_sheets_info = xlsx_to_json.get_sheet_info(temp_path)
            st.session_state.old_file_path = temp_path
            st.session_state.old_filename = old_file.name
            st.session_state.old_file_uploaded = True
        st.success(f"✅ OLD catalogue loaded: {old_file.name}")

# Handle NEW upload
if new_file:
    if not st.session_state.new_file_uploaded or st.session_state.get("new_filename") != new_file.name:
        with st.spinner("Analyzing NEW catalogue sheets..."):
            temp_path = f"/tmp/new_catalogue_{datetime.now().timestamp()}.xlsx"
            with open(temp_path, "wb") as f:
                f.write(new_file.getvalue())

            st.session_state.new_sheets_info = xlsx_to_json.get_sheet_info(temp_path)
            st.session_state.new_file_path = temp_path
            st.session_state.new_filename = new_file.name
            st.session_state.new_file_uploaded = True
        st.success(f"✅ NEW catalogue loaded: {new_file.name}")

st.markdown("---")


# ---------------------------------------------------------
# STEP 2 — SHEET MAPPING
# ---------------------------------------------------------
if st.session_state.old_file_uploaded and st.session_state.new_file_uploaded:
    st.subheader("📋 Step 2: Map Sheets")
    st.markdown("Select which sheets contain Current and Legacy items for each catalogue")

    tab_old, tab_new = st.tabs(["🗂️ OLD Catalogue", "🗂️ NEW Catalogue"])

    # -----------------------------------------------------
    # OLD CATALOGUE TAB
    # -----------------------------------------------------
    with tab_old:

        st.markdown(f"**File:** `{st.session_state.old_filename}`")

        st.markdown("**Available sheets:**")
        st.dataframe(pd.DataFrame(st.session_state.old_sheets_info), use_container_width=True, hide_index=True)
        st.markdown("**Select sheets:**")

        col1, col2 = st.columns(2)

        # CURRENT sheet
        with col1:
            st.markdown("**Current items sheet:**")
            opts = [s["name"] for s in st.session_state.old_sheets_info]

            default = None
            for s in opts:
                if "current" in s.lower() and "catalogue" not in s.lower():
                    default = s
                    break

            selected = st.selectbox(
                "Select CURRENT sheet",
                options=opts,
                index=opts.index(default) if default else 0,
                key="old_current_select",
                label_visibility="collapsed"
            )
            st.session_state.old_current_sheet = selected

        # LEGACY sheet (checkbox removed)
        with col2:
            st.markdown("**Legacy/deactivated items sheet:**")
            opts = [s["name"] for s in st.session_state.old_sheets_info]

            default = None
            for s in opts:
                if "legacy" in s.lower() or "deactivated" in s.lower():
                    default = s
                    break

            selected = st.selectbox(
                "Select LEGACY sheet",
                options=opts,
                index=opts.index(default) if default else 0,
                key="old_legacy_select",
                label_visibility="collapsed"
            )
            st.session_state.old_legacy_sheet = selected

        # PREVIEWS
        if st.session_state.old_current_sheet:
            with st.expander(f"Preview: {st.session_state.old_current_sheet} (first 5 rows)"):
                preview = xlsx_to_json.preview_sheet(st.session_state.old_file_path, st.session_state.old_current_sheet, 5)
                st.dataframe(preview, use_container_width=True)

        if st.session_state.old_legacy_sheet:
            with st.expander(f"Preview: {st.session_state.old_legacy_sheet} (first 5 rows)"):
                preview = xlsx_to_json.preview_sheet(st.session_state.old_file_path, st.session_state.old_legacy_sheet, 5)
                st.dataframe(preview, use_container_width=True)

    # -----------------------------------------------------
    # NEW CATALOGUE TAB
    # -----------------------------------------------------
    with tab_new:

        st.markdown(f"**File:** `{st.session_state.new_filename}`")

        st.markdown("**Available sheets:**")
        st.dataframe(pd.DataFrame(st.session_state.new_sheets_info), use_container_width=True, hide_index=True)
        st.markdown("**Select sheets:**")

        col1, col2 = st.columns(2)

        # CURRENT sheet
        with col1:
            st.markdown("**Current items sheet:**")
            opts = [s["name"] for s in st.session_state.new_sheets_info]

            default = None
            for s in opts:
                if "current" in s.lower() and "catalogue" not in s.lower():
                    default = s
                    break

            selected = st.selectbox(
                "Select CURRENT sheet",
                options=opts,
                index=opts.index(default) if default else 0,
                key="new_current_select",
                label_visibility="collapsed"
            )
            st.session_state.new_current_sheet = selected

        # LEGACY sheet (checkbox removed)
        with col2:
            st.markdown("**Legacy/deactivated items sheet:**")
            opts = [s["name"] for s in st.session_state.new_sheets_info]

            default = None
            for s in opts:
                if "legacy" in s.lower() or "deactivated" in s.lower():
                    default = s
                    break

            selected = st.selectbox(
                "Select LEGACY sheet",
                options=opts,
                index=opts.index(default) if default else 0,
                key="new_legacy_select",
                label_visibility="collapsed"
            )
            st.session_state.new_legacy_sheet = selected

        # PREVIEWS
        if st.session_state.new_current_sheet:
            with st.expander(f"Preview: {st.session_state.new_current_sheet} (first 5 rows)"):
                preview = xlsx_to_json.preview_sheet(st.session_state.new_file_path, st.session_state.new_current_sheet, 5)
                st.dataframe(preview, use_container_width=True)

        if st.session_state.new_legacy_sheet:
            with st.expander(f"Preview: {st.session_state.new_legacy_sheet} (first 5 rows)"):
                preview = xlsx_to_json.preview_sheet(st.session_state.new_file_path, st.session_state.new_legacy_sheet, 5)
                st.dataframe(preview, use_container_width=True)

    st.markdown("---")


    # ---------------------------------------------------------
    # STEP 3 — CONVERT & COMPARE
    # ---------------------------------------------------------
    st.subheader("🔧 Step 3: Convert & Compare")

    can_convert = (
        st.session_state.old_current_sheet is not None and
        st.session_state.new_current_sheet is not None
    )

    if can_convert:
        if st.button("🚀 Convert to JSON and Run Comparison", type="primary", use_container_width=True):
            with st.spinner("Converting catalogues to JSON..."):
                st.session_state.old_json = xlsx_to_json.convert_catalogue_to_json(
                    st.session_state.old_file_path,
                    st.session_state.old_current_sheet,
                    st.session_state.old_legacy_sheet,
                    st.session_state.old_filename
                )

                st.session_state.new_json = xlsx_to_json.convert_catalogue_to_json(
                    st.session_state.new_file_path,
                    st.session_state.new_current_sheet,
                    st.session_state.new_legacy_sheet,
                    st.session_state.new_filename
                )

            with st.spinner("Running comparison..."):
                st.session_state.comparison_results = version_diff.compare_catalogues(
                    st.session_state.old_json,
                    st.session_state.new_json
                )

            st.success("✅ Conversion and comparison complete!")
    else:
        st.warning("⚠️ Please select Current sheets for both catalogues before proceeding.")

    # ---------------------------------------------------------
    # STEP 4 — METADATA
    # ---------------------------------------------------------
    if st.session_state.old_json and st.session_state.new_json:
        st.markdown("---")
        st.subheader("📊 Results")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**OLD Catalogue Metadata**")
            st.json(st.session_state.old_json["metadata"])
            st.download_button(
                "📥 Download OLD JSON",
                json.dumps(st.session_state.old_json, indent=2),
                file_name=f"old_catalogue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        with col2:
            st.markdown("**NEW Catalogue Metadata**")
            st.json(st.session_state.new_json["metadata"])
            st.download_button(
                "📥 Download NEW JSON",
                json.dumps(st.session_state.new_json, indent=2),
                file_name=f"new_catalogue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    # ---------------------------------------------------------
    # STEP 5 — COMPARISON RESULTS
    # ---------------------------------------------------------
    if st.session_state.comparison_results:
        st.markdown("---")
        st.subheader("🔍 Comparison Results")

        summary = version_diff.get_comparison_summary(st.session_state.comparison_results)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Added", summary["added"])
        col2.metric("Removed", summary["removed"])
        col3.metric("Modified", summary["modified"])
        col4.metric("Unchanged", summary["unchanged"])

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Moved to Legacy", summary["moved_to_legacy"])
        col6.metric("Legacy Removed", summary["legacy_removed"])
        col7.metric("Anomalies", summary["anomalies"])
        col8.metric("Total Items", summary["total_items_compared"])

        st.markdown("---")

        results = st.session_state.comparison_results

        # Added
        if results["added"]:
            with st.expander(f"✅ Added Items ({len(results['added'])})"):
                df = pd.DataFrame([
                    {
                        "item_number": i["item_number"],
                        "support_name": i["item"].get("support_name", ""),
                        "category": i["item"].get("category", ""),
                        "unit": i["item"].get("unit", "")
                    }
                    for i in results["added"]
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

        # Removed
        if results["removed"]:
            with st.expander(f"❌ Removed from Current ({len(results['removed'])}) - Requires Review"):
                df = pd.DataFrame([
                    {
                        "item_number": i["item_number"],
                        "support_name": i["item"].get("support_name", ""),
                        "category": i["item"].get("category", ""),
                        "unit": i["item"].get("unit", "")
                    }
                    for i in results["removed"]
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

        # Moved to Legacy
        if results["moved_to_legacy"]:
            with st.expander(f"📦 Moved to Legacy ({len(results['moved_to_legacy'])})"):
                df = pd.DataFrame([
                    {
                        "item_number": i["item_number"],
                        "support_name": i["old_item"].get("support_name", ""),
                        "category": i["old_item"].get("category", "")
                    }
                    for i in results["moved_to_legacy"]
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

        # Legacy Removed
        if results["legacy_removed"]:
            with st.expander(f"🗑️ Legacy Removed ({len(results['legacy_removed'])})"):
                df = pd.DataFrame([
                    {
                        "item_number": i["item_number"],
                        "support_name": i["item"].get("support_name", ""),
                        "category": i["item"].get("category", "")
                    }
                    for i in results["legacy_removed"]
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

        # Modified
        if results["modified"]:
            with st.expander(f"✏️ Modified Items ({len(results['modified'])})", expanded=True):
                df = pd.DataFrame(version_diff.create_modified_items_table(results["modified"]))
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.download_button(
                    "📥 Download modified items (JSON)",
                    json.dumps(results["modified"], indent=2),
                    file_name=f"modified_items_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        # Unchanged
        if results["unchanged"]:
            with st.expander(f"✓ Unchanged Items ({len(results['unchanged'])})"):
                df = pd.DataFrame([
                    {
                        "item_number": i["item_number"],
                        "support_name": i["item"].get("support_name", ""),
                        "category": i["item"].get("category", "")
                    }
                    for i in results["unchanged"]
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

        # Anomalies
        if results["anomalies"]:
            with st.expander(f"⚠️ Anomalies ({len(results['anomalies'])})"):
                df = pd.DataFrame([
                    {
                        "item_number": i["item_number"],
                        "description": i["description"]
                    }
                    for i in results["anomalies"]
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.info("👆 Upload both OLD and NEW catalogue files to begin")
