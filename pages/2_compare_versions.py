import json
import sys
import uuid
from pathlib import Path
import streamlit as st

# Local imports
sys.path.append("/app")
from version_diff import diff_catalogues, diff_to_markdown, generate_pdf_from_markdown, STATES


# ---------------------------------------------------------
# LOAD NDIA THEME
# ---------------------------------------------------------
def load_theme():
    candidates = [
        Path(__file__).resolve().parents[1] / "ndis_theme.css",
        Path("/app/ndis_theme.css")
    ]
    for c in candidates:
        if c.exists():
            st.markdown(f"<style>{c.read_text()}</style>", unsafe_allow_html=True)
            return
    st.warning("⚠️ Could not load ndis_theme.css")

load_theme()


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Compare Support Catalogue Versions",
    page_icon="🔍",
    layout="wide",
)


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def load_json(upload):
    return json.loads(upload.read().decode("utf-8"))


def paginated_dataframe(rows, page_size=20):
    """Safe Streamlit pagination with unique widget IDs."""
    if not rows:
        st.write("No rows to display.")
        return

    unique = str(uuid.uuid4())
    total_rows = len(rows)
    total_pages = max(1, (total_rows - 1) // page_size + 1)

    col1, col2 = st.columns([1, 4])

    with col1:
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
            key=f"page_{unique}"
        )

    st.dataframe(rows[(page - 1) * page_size : (page * page_size)], use_container_width=True)


def serialisable_diff(diff):
    """Convert diff object to JSON."""
    return {
        "summary": {
            "added": diff.added_count,
            "removed": diff.removed_count,
            "modified": diff.modified_count,
            "unchanged": diff.unchanged_count,
            "old_version": diff.old_version,
            "new_version": diff.new_version,
        },
        "added_items": diff.added_items,
        "removed_items": diff.removed_items,
        "modified_items": [
            {
                "support_item_number": m.support_item_number,
                "name": m.name,
                "price_changes": {
                    s: {
                        "old": pc.old,
                        "new": pc.new,
                        "change_pct": pc.change_pct
                    }
                    for s, pc in m.price_changes.items()
                },
                "claim_type_changes": {
                    ct: {"old": ctchg.old, "new": ctchg.new}
                    for ct, ctchg in m.claim_type_changes.items()
                },
            }
            for m in diff.modified_items
        ]
    }


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------
st.markdown("<div class='nids-main-title'>Compare Support Catalogue Versions</div>", unsafe_allow_html=True)
st.markdown("<div class='nids-subtitle'>Upload two catalogue JSON files to identify added, removed and modified support items.</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("Version Comparison")

old_file = st.sidebar.file_uploader("Old version (JSON)", type=["json"])
new_file = st.sidebar.file_uploader("New version (JSON)", type=["json"])
state_for_table = st.sidebar.selectbox("State for price comparisons", STATES, index=1)
run_button = st.sidebar.button("Run comparison", type="primary")

if not (old_file and new_file):
    st.info("Upload both versions to begin.")
    st.stop()


# ---------------------------------------------------------
# RUN DIFF
# ---------------------------------------------------------
if run_button:
    with st.spinner("Computing differences…"):
        old_catalogue = load_json(old_file)
        new_catalogue = load_json(new_file)
        diff = diff_catalogues(old_catalogue, new_catalogue)

    # EXEC SUMMARY
    st.markdown("<div class='nids-section-header'>Executive Summary</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Added", diff.added_count)
    c2.metric("Removed", diff.removed_count)
    c3.metric("Modified", diff.modified_count)
    c4.metric("Unchanged", diff.unchanged_count)

    st.write(f"**Old version:** `{diff.old_version}`")
    st.write(f"**New version:** `{diff.new_version}`")

    # PRICE STATS
    st.markdown("<div class='nids-section-header'>Price Change Statistics by State</div>", unsafe_allow_html=True)

    if diff.price_stats_by_state:
        rows = []
        for state, s in diff.price_stats_by_state.items():
            rows.append({
                "State": state,
                "Items changed": s.count,
                "Avg %": f"{s.avg:+.2f}%",
                "Min %": f"{s.min:+.2f}%",
                "Max %": f"{s.max:+.2f}%",
                "+": s.increases,
                "-": s.decreases,
            })
        st.dataframe(rows, use_container_width=True)
    else:
        st.info("No price changes detected.")

    # ADDED ITEMS
    st.markdown("<div class='nids-section-header'>Added Items</div>", unsafe_allow_html=True)

    added_rows = [
        {
            "Support item number": i["support_item_number"],
            "Name": i["support_item_name"],
            "Category": i["support_category_name"],
            f"{state_for_table} price": i["price_limits"].get(state_for_table),
        }
        for i in diff.added_items
    ]

    with st.expander(f"View added items ({len(added_rows)})"):
        paginated_dataframe(added_rows)

    # REMOVED ITEMS
    st.markdown("<div class='nids-section-header'>Removed Items</div>", unsafe_allow_html=True)

    removed_rows = [
        {
            "Support item number": i["support_item_number"],
            "Name": i["support_item_name"],
            "Category": i["support_category_name"],
            f"{state_for_table} price (old)": i["price_limits"].get(state_for_table),
        }
        for i in diff.removed_items
    ]

    with st.expander(f"View removed items ({len(removed_rows)})"):
        paginated_dataframe(removed_rows)

    # PRICE CHANGES
    st.markdown(f"<div class='nids-section-header'>Price Changes — {state_for_table}</div>", unsafe_allow_html=True)

    price_change_rows = []
    for m in diff.modified_items:
        if pc := m.price_changes.get(state_for_table):
            price_change_rows.append({
                "Support item number": m.support_item_number,
                "Name": m.name,
                "Old": pc.old,
                "New": pc.new,
                "Change %": round(pc.change_pct, 2),
                "Direction": "Increase" if pc.change_pct > 0 else "Decrease",
            })

    with st.expander(f"View price changes ({len(price_change_rows)})"):
        paginated_dataframe(price_change_rows)

    # CLAIM TYPE CHANGES
    st.markdown("<div class='nids-section-header'>Claim Type Changes</div>", unsafe_allow_html=True)

    claim_rows = []
    for m in diff.modified_items:
        for ct, ch in m.claim_type_changes.items():
            claim_rows.append({
                "Support item number": m.support_item_number,
                "Name": m.name,
                "Claim type": ct.replace("_", " ").title(),
                "Old": "Yes" if ch.old else "No",
                "New": "Yes" if ch.new else "No",
            })

    with st.expander(f"View claim type changes ({len(claim_rows)})"):
        paginated_dataframe(claim_rows)

    # EXPORTS
    st.markdown("<div class='nids-section-header'>Exports</div>", unsafe_allow_html=True)

    md_report = diff_to_markdown(diff)
    pdf_report = generate_pdf_from_markdown(md_report)
    json_payload = json.dumps(serialisable_diff(diff), indent=2)

    colA, colB, colC = st.columns(3)

    with colA:
        st.download_button("⬇️ Markdown", md_report, "catalogue-diff.md", "text/markdown")

    with colB:
        st.download_button("⬇️ JSON", json_payload, "catalogue-diff.json", "application/json")

    with colC:
        st.download_button("⬇️ PDF", pdf_report, "catalogue-diff.pdf", "application/pdf")
