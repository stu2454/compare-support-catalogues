"""
Version Comparison Logic for NDIS Support Catalogue

Handles 7 scenarios:
1. Added - present only in NEW Current
2. Removed from Current (no legacy) - present in OLD Current, absent from NEW
3. Moved to Legacy - present in OLD Current, present in NEW Legacy, absent from NEW Current
4. Legacy removed - present only in OLD Legacy, absent from NEW
5. Modified - present in both Current with field-level changes
6. Unchanged - present in both Current with no changes
7. Anomalies - odd transitions requiring review
"""

from typing import Dict, List, Set


def _normalize_for_comparison(value) -> str:
    """
    Normalize a value for comparison to avoid false positives.
    - Strips whitespace
    - Lowercases strings
    - Converts None to empty string
    """
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip().lower()
    return str(value)


def _compute_field_changes(old_item: Dict, new_item: Dict) -> Dict[str, Dict[str, any]]:
    """
    Compare two items field-by-field and return a dict of changes.
    
    Returns:
        {
            'field_name': {
                'old': old_value,
                'new': new_value
            },
            ...
        }
    """
    changes = {}
    
    # All possible fields to compare (excluding raw_row_index which is metadata)
    fields_to_compare = [
        'support_name', 'registration_group', 'category', 'unit', 'claim_type',
        'price_limit_nsw', 'price_limit_vic', 'price_limit_qld', 'price_limit_sa',
        'price_limit_wa', 'price_limit_tas', 'price_limit_nt', 'price_limit_act',
        'effective_from', 'effective_to', 'notes'
    ]
    
    for field in fields_to_compare:
        old_val = old_item.get(field)
        new_val = new_item.get(field)
        
        # Normalize for comparison
        old_normalized = _normalize_for_comparison(old_val)
        new_normalized = _normalize_for_comparison(new_val)
        
        if old_normalized != new_normalized:
            changes[field] = {
                'old': old_val,
                'new': new_val
            }
    
    return changes


def _index_catalogue(catalogue: Dict) -> Dict[str, Dict]:
    """
    Index a catalogue by item_number for quick lookup.
    
    Returns:
        {
            'item_number': {
                'current': item_dict or None,
                'legacy': item_dict or None
            },
            ...
        }
    """
    index = {}
    
    # Index current items
    for item in catalogue.get('current_items', []):
        item_num = item.get('item_number')
        if item_num:
            if item_num not in index:
                index[item_num] = {'current': None, 'legacy': None}
            index[item_num]['current'] = item
    
    # Index legacy items
    for item in catalogue.get('legacy_items', []):
        item_num = item.get('item_number')
        if item_num:
            if item_num not in index:
                index[item_num] = {'current': None, 'legacy': None}
            index[item_num]['legacy'] = item
    
    return index


def compare_catalogues(old_cat: Dict, new_cat: Dict) -> Dict:
    """
    Compare two catalogues and categorize all changes.
    
    Returns:
        {
            'added': [...],                # Present only in NEW Current
            'removed': [...],              # Present in OLD Current, absent from NEW (no legacy)
            'moved_to_legacy': [...],      # Present in OLD Current, now in NEW Legacy
            'legacy_removed': [...],       # Present in OLD Legacy, absent from NEW
            'modified': [...],             # In both Current, with field changes
            'unchanged': [...],            # In both Current, no changes
            'anomalies': [...]             # Odd transitions requiring review
        }
    """
    old_index = _index_catalogue(old_cat)
    new_index = _index_catalogue(new_cat)
    
    # Get all item numbers across both catalogues
    all_item_numbers = set(old_index.keys()) | set(new_index.keys())
    
    results = {
        'added': [],
        'removed': [],
        'moved_to_legacy': [],
        'legacy_removed': [],
        'modified': [],
        'unchanged': [],
        'anomalies': []
    }
    
    for item_num in all_item_numbers:
        old_entry = old_index.get(item_num, {'current': None, 'legacy': None})
        new_entry = new_index.get(item_num, {'current': None, 'legacy': None})
        
        old_current = old_entry['current']
        old_legacy = old_entry['legacy']
        new_current = new_entry['current']
        new_legacy = new_entry['legacy']
        
        # SCENARIO 1: Added
        # Present only in NEW Current, not in OLD at all
        if new_current and not old_current and not old_legacy:
            results['added'].append({
                'item_number': item_num,
                'item': new_current
            })
        
        # SCENARIO 2: Removed from Current (no legacy)
        # Present in OLD Current, absent from NEW Current and NEW Legacy
        elif old_current and not new_current and not new_legacy:
            results['removed'].append({
                'item_number': item_num,
                'item': old_current,
                'requires_review': True  # Governance risk
            })
        
        # SCENARIO 3: Moved to Legacy
        # Present in OLD Current, present in NEW Legacy, absent from NEW Current
        elif old_current and new_legacy and not new_current:
            results['moved_to_legacy'].append({
                'item_number': item_num,
                'old_item': old_current,
                'new_legacy_item': new_legacy
            })
        
        # SCENARIO 4: Legacy removed
        # Present only in OLD Legacy, absent from NEW entirely
        elif old_legacy and not new_current and not new_legacy:
            results['legacy_removed'].append({
                'item_number': item_num,
                'item': old_legacy
            })
        
        # SCENARIO 5 & 6: Modified or Unchanged
        # Present in OLD Current and NEW Current
        elif old_current and new_current:
            changes = _compute_field_changes(old_current, new_current)
            
            if changes:
                # Modified
                results['modified'].append({
                    'item_number': item_num,
                    'old': old_current,
                    'new': new_current,
                    'changes': changes
                })
            else:
                # Unchanged
                results['unchanged'].append({
                    'item_number': item_num,
                    'item': new_current
                })
        
        # SCENARIO 7: Anomalies
        # Any other weird combination
        else:
            anomaly_desc = []
            if old_current:
                anomaly_desc.append("OLD Current")
            if old_legacy:
                anomaly_desc.append("OLD Legacy")
            if new_current:
                anomaly_desc.append("NEW Current")
            if new_legacy:
                anomaly_desc.append("NEW Legacy")
            
            results['anomalies'].append({
                'item_number': item_num,
                'old_current': old_current,
                'old_legacy': old_legacy,
                'new_current': new_current,
                'new_legacy': new_legacy,
                'description': f"Unusual transition: {' → '.join(anomaly_desc)}"
            })
    
    return results


def create_modified_items_table(modified_items: List[Dict]) -> List[Dict]:
    """
    Convert modified items into a flat table format for display.
    
    Each row represents one field change for one item.
    
    Returns:
        [
            {
                'item_number': '05_123456',
                'field': 'support_name',
                'old_value': 'Old description',
                'new_value': 'New description'
            },
            ...
        ]
    """
    rows = []
    
    for modified in modified_items:
        item_num = modified['item_number']
        changes = modified['changes']
        
        for field, change_info in changes.items():
            rows.append({
                'item_number': item_num,
                'field': field,
                'old_value': change_info['old'],
                'new_value': change_info['new']
            })
    
    return rows


def get_comparison_summary(comparison_results: Dict) -> Dict[str, int]:
    """
    Get summary statistics from comparison results.
    
    Returns:
        {
            'added': count,
            'removed': count,
            'moved_to_legacy': count,
            'legacy_removed': count,
            'modified': count,
            'unchanged': count,
            'anomalies': count,
            'total_items_compared': count
        }
    """
    summary = {
        'added': len(comparison_results['added']),
        'removed': len(comparison_results['removed']),
        'moved_to_legacy': len(comparison_results['moved_to_legacy']),
        'legacy_removed': len(comparison_results['legacy_removed']),
        'modified': len(comparison_results['modified']),
        'unchanged': len(comparison_results['unchanged']),
        'anomalies': len(comparison_results['anomalies'])
    }
    
    summary['total_items_compared'] = sum(summary.values())
    
    return summary
