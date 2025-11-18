#!/usr/bin/env python3
"""
NDIS Support Catalogue XLSX to JSON Parser
"""

import json
from pathlib import Path
from datetime import datetime

import openpyxl


# -----------------------
# Helper parsing functions
# -----------------------

def parse_boolean_field(value) -> bool:
    """Convert Excel Yes/No/Y/N values to boolean."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    str_val = str(value).strip().upper()
    return str_val in ['YES', 'Y', 'TRUE', '1']


def parse_price(value):
    """Parse price value, handling None and invalid values."""
    if value is None or value == '' or value == 'N/A':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_date(value) -> str:
    """Convert date value to YYYYMMDD or keep string."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return str(int(value))
    if hasattr(value, "strftime"):
        return value.strftime("%Y%m%d")
    return str(value)


# -----------------------
# Row conversion
# -----------------------

def convert_row_to_support_item(row_data: dict, row_number: int) -> dict:
    """Convert a single Excel row to JSON structure."""

    support_item = {
        "support_item_number": str(row_data.get("Support Item Number", "")).strip(),
        "support_item_name": str(row_data.get("Support Item Name", "")).strip(),
        "registration_group_number": str(row_data.get("Registration Group Number", "")).strip(),
        "registration_group_name": str(row_data.get("Registration Group Name", "")).strip(),
        "support_category_number": int(row_data.get("Support Category Number", 0)),
        "support_category_number_pace": row_data.get("Support Category Number (PACE)"),
        "support_category_name": str(row_data.get("Support Category Name", "")).strip(),
        "support_category_name_pace": row_data.get("Support Category Name (PACE)"),
        "unit": str(row_data.get("Unit", "")).strip(),
        "quote": parse_boolean_field(row_data.get("Quote")),
        "price_limits": {
            "ACT": parse_price(row_data.get("ACT")),
            "NSW": parse_price(row_data.get("NSW")),
            "NT": parse_price(row_data.get("NT")),
            "QLD": parse_price(row_data.get("QLD")),
            "SA": parse_price(row_data.get("SA")),
            "TAS": parse_price(row_data.get("TAS")),
            "VIC": parse_price(row_data.get("VIC")),
            "WA": parse_price(row_data.get("WA")),
            "remote": parse_price(row_data.get("Remote")),
            "very_remote": parse_price(row_data.get("Very Remote"))
        },
        "claim_types": {
            "standard": True,
            "cancellation": parse_boolean_field(row_data.get("Short Notice Cancellations.")),
            "travel": parse_boolean_field(row_data.get("Provider Travel")),
            "non_face_to_face": parse_boolean_field(row_data.get("Non-Face-to-Face Support Provision")),
            "telehealth": False,
            "irregular_sil_supports": parse_boolean_field(row_data.get("Irregular SIL Supports")),
            "ndia_requested_reports": parse_boolean_field(row_data.get("NDIA Requested Reports"))
        },
        "support_item_type": row_data.get("Type"),
        "effective_from": parse_date(row_data.get("Start date")),
        "effective_to": parse_date(row_data.get("End Date")),
        "source_row": row_number
    }

    # Cleanup PACE fields
    try:
        if support_item["support_category_number_pace"] is not None:
            support_item["support_category_number_pace"] = int(support_item["support_category_number_pace"])
    except (ValueError, TypeError):
        support_item["support_category_number_pace"] = None

    if support_item["support_category_name_pace"]:
        support_item["support_category_name_pace"] = str(support_item["support_category_name_pace"]).strip()

    if support_item["support_item_type"]:
        support_item["support_item_type"] = str(support_item["support_item_type"]).strip()

    return support_item


# -----------------------
# Main parser
# -----------------------

def parse_xlsx_to_json(xlsx_path: str, sheet_name: str = "Current Support Items") -> dict:
    """Parse NDIS Support Catalogue Excel file to JSON."""

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)

    if sheet_name not in wb.sheetnames:
        raise ValueError(f"Sheet '{sheet_name}' not found. Available: {wb.sheetnames}")

    ws = wb[sheet_name]

    # Extract headers
    headers = [cell.value for cell in ws[1]]

    support_items = []
    errors = []

    for row_idx in range(2, ws.max_row + 1):
        row_values = [cell.value for cell in ws[row_idx]]

        if not any(row_values):
            continue

        row_data = dict(zip(headers, row_values))

        if not row_data.get("Support Item Number"):
            continue

        try:
            support_item = convert_row_to_support_item(row_data, row_idx)
            support_items.append(support_item)
        except Exception as e:
            errors.append({"row": row_idx, "error": str(e)})

    catalogue = {
        "metadata": {
            "source_file": Path(xlsx_path).name,
            "source_sheet": sheet_name,
            "generated_at": datetime.now().isoformat(),
            "total_items": len(support_items),
            "conversion_errors": len(errors),
        },
        "support_items": support_items,
    }

    if errors:
        catalogue["metadata"]["errors"] = errors

    return catalogue

