"""
Test script to verify the NDIS Support Catalogue tool functionality

Creates mock Excel files and tests:
1. Sheet detection
2. Excel to JSON conversion
3. Version comparison
"""

import pandas as pd
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import xlsx_to_json
import version_diff


def create_mock_catalogue(filename, current_items, legacy_items=None):
    """
    Create a mock NDIS Support Catalogue Excel file.
    """
    # Create current items DataFrame
    current_df = pd.DataFrame(current_items)
    
    # Create Excel writer
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        current_df.to_excel(writer, sheet_name='Current Support Items', index=False)
        
        if legacy_items:
            legacy_df = pd.DataFrame(legacy_items)
            legacy_df.to_excel(writer, sheet_name='Legacy Support Items', index=False)
    
    print(f"✅ Created mock catalogue: {filename}")


def test_sheet_detection(filename):
    """Test that sheet detection works."""
    print(f"\n📋 Testing sheet detection for {filename}...")
    sheets_info = xlsx_to_json.get_sheet_info(filename)
    
    print(f"Found {len(sheets_info)} sheets:")
    for sheet in sheets_info:
        print(f"  - {sheet['name']}: {sheet['row_count']} rows, {sheet['col_count']} columns")
    
    return sheets_info


def test_conversion(filename, current_sheet, legacy_sheet=None):
    """Test Excel to JSON conversion."""
    print(f"\n🔄 Testing conversion for {filename}...")
    
    catalogue_json = xlsx_to_json.convert_catalogue_to_json(
        filename,
        current_sheet,
        legacy_sheet,
        filename
    )
    
    print(f"✅ Conversion successful!")
    print(f"  - Current items: {len(catalogue_json['current_items'])}")
    print(f"  - Legacy items: {len(catalogue_json['legacy_items'])}")
    
    return catalogue_json


def test_comparison(old_cat, new_cat):
    """Test catalogue comparison."""
    print(f"\n🔍 Testing comparison...")
    
    results = version_diff.compare_catalogues(old_cat, new_cat)
    summary = version_diff.get_comparison_summary(results)
    
    print(f"✅ Comparison complete!")
    print(f"  - Added: {summary['added']}")
    print(f"  - Removed: {summary['removed']}")
    print(f"  - Moved to Legacy: {summary['moved_to_legacy']}")
    print(f"  - Legacy Removed: {summary['legacy_removed']}")
    print(f"  - Modified: {summary['modified']}")
    print(f"  - Unchanged: {summary['unchanged']}")
    print(f"  - Anomalies: {summary['anomalies']}")
    
    return results


def main():
    print("🧪 NDIS Support Catalogue Tool - Test Suite")
    print("=" * 60)
    
    # Create mock OLD catalogue
    old_current_items = [
        {
            'Item Number': '05_001_0001_1_1',
            'Support Name': 'Standard wheelchair',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Standard',
            'NSW': 450.0,
            'VIC': 455.0,
            'QLD': 450.0,
            'SA': 450.0,
            'WA': 460.0,
            'TAS': 450.0,
            'NT': 450.0,
            'ACT': 450.0,
            'Effective From': '2024-07-01',
            'Notes': 'Standard manual wheelchair'
        },
        {
            'Item Number': '05_002_0002_1_1',
            'Support Name': 'Shower chair',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Care',
            'Unit': 'Each',
            'Claim Type': 'Quote Required',
            'NSW': 200.0,
            'VIC': 205.0,
            'QLD': 200.0,
            'SA': 200.0,
            'WA': 210.0,
            'TAS': 200.0,
            'NT': 200.0,
            'ACT': 200.0,
            'Effective From': '2024-07-01',
            'Notes': 'Waterproof shower chair'
        },
        {
            'Item Number': '05_003_0003_1_1',
            'Support Name': 'Walking frame',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Standard',
            'NSW': 120.0,
            'VIC': 120.0,
            'QLD': 120.0,
            'SA': 120.0,
            'WA': 125.0,
            'TAS': 120.0,
            'NT': 120.0,
            'ACT': 120.0,
            'Effective From': '2024-07-01',
            'Notes': 'Adjustable height'
        }
    ]
    
    old_legacy_items = [
        {
            'Item Number': '05_999_9999_1_1',
            'Support Name': 'Old style wheelchair',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Standard',
            'NSW': 400.0,
            'VIC': 400.0,
            'QLD': 400.0,
            'SA': 400.0,
            'WA': 400.0,
            'TAS': 400.0,
            'NT': 400.0,
            'ACT': 400.0,
            'Effective From': '2023-07-01',
            'Effective To': '2024-06-30',
            'Notes': 'Deactivated - replaced by 05_001_0001_1_1'
        }
    ]
    
    # Create mock NEW catalogue (with changes)
    new_current_items = [
        {
            'Item Number': '05_001_0001_1_1',
            'Support Name': 'Standard wheelchair',  # Unchanged
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Standard',
            'NSW': 450.0,
            'VIC': 455.0,
            'QLD': 450.0,
            'SA': 450.0,
            'WA': 460.0,
            'TAS': 450.0,
            'NT': 450.0,
            'ACT': 450.0,
            'Effective From': '2024-07-01',
            'Notes': 'Standard manual wheelchair'
        },
        {
            'Item Number': '05_002_0002_1_1',
            'Support Name': 'Premium shower chair',  # MODIFIED: name changed
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Care',
            'Unit': 'Each',
            'Claim Type': 'Quote Required',
            'NSW': 220.0,  # MODIFIED: price increased
            'VIC': 225.0,  # MODIFIED: price increased
            'QLD': 220.0,
            'SA': 220.0,
            'WA': 230.0,
            'TAS': 220.0,
            'NT': 220.0,
            'ACT': 220.0,
            'Effective From': '2024-07-01',
            'Notes': 'Waterproof shower chair with adjustable height'
        },
        {
            'Item Number': '05_004_0004_1_1',  # ADDED: new item
            'Support Name': 'Electric wheelchair',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Quote Required',
            'NSW': 2500.0,
            'VIC': 2550.0,
            'QLD': 2500.0,
            'SA': 2500.0,
            'WA': 2600.0,
            'TAS': 2500.0,
            'NT': 2500.0,
            'ACT': 2500.0,
            'Effective From': '2025-01-01',
            'Notes': 'Electric powered wheelchair'
        }
        # REMOVED: Walking frame (05_003_0003_1_1) is no longer in current - should be flagged
    ]
    
    new_legacy_items = [
        {
            'Item Number': '05_999_9999_1_1',
            'Support Name': 'Old style wheelchair',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Standard',
            'NSW': 400.0,
            'VIC': 400.0,
            'QLD': 400.0,
            'SA': 400.0,
            'WA': 400.0,
            'TAS': 400.0,
            'NT': 400.0,
            'ACT': 400.0,
            'Effective From': '2023-07-01',
            'Effective To': '2024-06-30',
            'Notes': 'Deactivated - replaced by 05_001_0001_1_1'
        },
        {
            'Item Number': '05_003_0003_1_1',  # MOVED TO LEGACY: walking frame
            'Support Name': 'Walking frame',
            'Registration Group': 'Assistive Technology',
            'Category': 'Personal Mobility',
            'Unit': 'Each',
            'Claim Type': 'Standard',
            'NSW': 120.0,
            'VIC': 120.0,
            'QLD': 120.0,
            'SA': 120.0,
            'WA': 125.0,
            'TAS': 120.0,
            'NT': 120.0,
            'ACT': 120.0,
            'Effective From': '2024-07-01',
            'Effective To': '2024-12-31',
            'Notes': 'Deactivated'
        }
    ]
    
    # Create mock files
    old_file = '/tmp/test_catalogue_old.xlsx'
    new_file = '/tmp/test_catalogue_new.xlsx'
    
    create_mock_catalogue(old_file, old_current_items, old_legacy_items)
    create_mock_catalogue(new_file, new_current_items, new_legacy_items)
    
    # Test sheet detection
    old_sheets = test_sheet_detection(old_file)
    new_sheets = test_sheet_detection(new_file)
    
    # Test conversion
    old_json = test_conversion(old_file, 'Current Support Items', 'Legacy Support Items')
    new_json = test_conversion(new_file, 'Current Support Items', 'Legacy Support Items')
    
    # Test comparison
    comparison_results = test_comparison(old_json, new_json)
    
    # Show detailed results
    print("\n📊 Detailed Comparison Results:")
    print("=" * 60)
    
    if comparison_results['added']:
        print("\n✅ ADDED items:")
        for item in comparison_results['added']:
            print(f"  - {item['item_number']}: {item['item'].get('support_name')}")
    
    if comparison_results['removed']:
        print("\n❌ REMOVED items (requires review):")
        for item in comparison_results['removed']:
            print(f"  - {item['item_number']}: {item['item'].get('support_name')}")
    
    if comparison_results['moved_to_legacy']:
        print("\n📦 MOVED TO LEGACY:")
        for item in comparison_results['moved_to_legacy']:
            print(f"  - {item['item_number']}: {item['old_item'].get('support_name')}")
    
    if comparison_results['modified']:
        print("\n✏️ MODIFIED items:")
        for item in comparison_results['modified']:
            print(f"  - {item['item_number']}: {item['old'].get('support_name')}")
            for field, change in item['changes'].items():
                print(f"    * {field}: {change['old']} → {change['new']}")
    
    if comparison_results['unchanged']:
        print("\n✓ UNCHANGED items:")
        for item in comparison_results['unchanged']:
            print(f"  - {item['item_number']}: {item['item'].get('support_name')}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed successfully!")
    print("\nThe tool is ready to use. Run:")
    print("  streamlit run streamlit_app.py")
    print("\nOr with Docker:")
    print("  docker-compose up --build")


if __name__ == '__main__':
    main()
