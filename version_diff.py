"""
Version diff utilities for NDIS Support Catalogue JSON files.

This version:
- Pure Python only
- No Cairo / xhtml2pdf dependencies
- Adds Markdown → PDF export using ReportLab canvas
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import statistics
import markdown
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


STATES = [
    "ACT", "NSW", "NT", "QLD", "SA", "TAS",
    "VIC", "WA", "remote", "very_remote"
]


# ---------------------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------------------

@dataclass
class PriceChange:
    state: str
    old: float
    new: float
    change_pct: float


@dataclass
class ClaimTypeChange:
    claim_type: str
    old: bool
    new: bool


@dataclass
class ItemChange:
    support_item_number: str
    name: str
    price_changes: Dict[str, PriceChange]
    claim_type_changes: Dict[str, ClaimTypeChange]


@dataclass
class StateStats:
    count: int
    avg: float
    min: float
    max: float
    increases: int
    decreases: int


@dataclass
class CatalogueDiff:
    old_version: str
    new_version: str
    added_items: List[Dict[str, Any]]
    removed_items: List[Dict[str, Any]]
    modified_items: List[ItemChange]
    unchanged_count: int
    price_stats_by_state: Dict[str, StateStats]

    @property
    def added_count(self) -> int:
        return len(self.added_items)

    @property
    def removed_count(self) -> int:
        return len(self.removed_items)

    @property
    def modified_count(self) -> int:
        return len(self.modified_items)

    @property
    def total_changes(self) -> int:
        return self.added_count + self.removed_count + self.modified_count


# ---------------------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------------------

def _build_item_index(catalogue: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index = {}
    for item in catalogue.get("support_items", []):
        num = item.get("support_item_number")
        if num:
            index[str(num)] = item
    return index


# ---------------------------------------------------------------------
# DIFF LOGIC
# ---------------------------------------------------------------------

def diff_catalogues(old: Dict[str, Any], new: Dict[str, Any]) -> CatalogueDiff:
    old_items = _build_item_index(old)
    new_items = _build_item_index(new)

    old_keys = set(old_items.keys())
    new_keys = set(new_items.keys())

    added_keys = sorted(new_keys - old_keys)
    removed_keys = sorted(old_keys - new_keys)
    common_keys = sorted(old_keys & new_keys)

    added_items = [new_items[k] for k in added_keys]
    removed_items = [old_items[k] for k in removed_keys]

    modified_items: List[ItemChange] = []
    all_price_changes = []

    for key in common_keys:
        o = old_items[key]
        n = new_items[key]

        price_diffs = {}
        claim_diffs = {}

        # Price diffs
        for state in STATES:
            prev = o.get("price_limits", {}).get(state)
            newp = n.get("price_limits", {}).get(state)

            if (
                prev is not None and newp is not None
                and prev != 0 and newp != prev
            ):
                pct = (newp - prev) / prev * 100
                ch = PriceChange(state, float(prev), float(newp), pct)
                price_diffs[state] = ch
                all_price_changes.append(ch)

        # Claim type diffs
        old_claims = o.get("claim_types", {}) or {}
        new_claims = n.get("claim_types", {}) or {}

        for ct in set(old_claims) | set(new_claims):
            prev_val = bool(old_claims.get(ct, False))
            new_val = bool(new_claims.get(ct, False))
            if prev_val != new_val:
                claim_diffs[ct] = ClaimTypeChange(ct, prev_val, new_val)

        if price_diffs or claim_diffs:
            modified_items.append(ItemChange(
                support_item_number=key,
                name=n.get("support_item_name", o.get("support_item_name")),
                price_changes=price_diffs,
                claim_type_changes=claim_diffs,
            ))

    unchanged_count = len(common_keys) - len(modified_items)

    # State-level stats
    stats = {}
    for state in STATES:
        changes = [pc for pc in all_price_changes if pc.state == state]
        if not changes:
            continue

        pct_list = [pc.change_pct for pc in changes]
        stats[state] = StateStats(
            count=len(pct_list),
            avg=statistics.mean(pct_list),
            min=min(pct_list),
            max=max(pct_list),
            increases=sum(1 for p in pct_list if p > 0),
            decreases=sum(1 for p in pct_list if p < 0)
        )

    return CatalogueDiff(
        old_version=old.get("metadata", {}).get("catalogue_version", "unknown"),
        new_version=new.get("metadata", {}).get("catalogue_version", "unknown"),
        added_items=added_items,
        removed_items=removed_items,
        modified_items=modified_items,
        unchanged_count=unchanged_count,
        price_stats_by_state=stats
    )


# ---------------------------------------------------------------------
# MARKDOWN REPORT GENERATOR
# ---------------------------------------------------------------------

def diff_to_markdown(diff: CatalogueDiff) -> str:
    """Convert the diff into a Markdown report."""
    lines = []
    lines.append("# NDIS Support Catalogue Version Comparison Report\n")
    lines.append(f"- **Old Version:** {diff.old_version}")
    lines.append(f"- **New Version:** {diff.new_version}\n")

    lines.append("## Executive Summary\n")
    lines.append("| Change Type | Count |")
    lines.append("|-------------|-------|")
    lines.append(f"| Items Added | {diff.added_count} |")
    lines.append(f"| Items Removed | {diff.removed_count} |")
    lines.append(f"| Items Modified | {diff.modified_count} |")
    lines.append(f"| Items Unchanged | {diff.unchanged_count} |")
    lines.append(f"| **Total Changes** | **{diff.total_changes}** |")
    lines.append("")

    if diff.price_stats_by_state:
        lines.append("## Price Change Statistics by State\n")
        lines.append("| State | Items Changed | Avg % | Min % | Max % | + | - |")
        lines.append("|-------|--------------|-------|-------|-------|---|---|")
        for state, s in diff.price_stats_by_state.items():
            def fmt(x):
                return f"{x:+.2f}%"
            lines.append(
                f"| {state} | {s.count} | {fmt(s.avg)} | {fmt(s.min)} | {fmt(s.max)} | {s.increases} | {s.decreases} |"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------
# PDF GENERATOR (pure Python, Streamlit + Docker friendly)
# ---------------------------------------------------------------------

def generate_pdf_from_markdown(md_text: str) -> bytes:
    """
    Convert markdown → text → PDF using a simple ReportLab layout.
    This avoids Cairo/wkhtmltopdf and works in slim containers.
    """

    # Convert Markdown to plain text (remove HTML)
    html = markdown.markdown(md_text)
    import re
    text = re.sub(r"<[^>]+>", "", html)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    textobject = c.beginText(40, 750)
    textobject.setFont("Helvetica", 10)

    # Basic line wrapping
    for line in text.split("\n"):
        while len(line) > 95:
            textobject.textLine(line[:95])
            line = line[95:]
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    c.save()

    return buffer.getvalue()
