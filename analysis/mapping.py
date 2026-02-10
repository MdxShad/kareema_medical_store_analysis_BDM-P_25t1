from __future__ import annotations
from typing import Dict, List

ALIASES = {
    'category': ['therapeutic tag', 'category', 'class', 'segment'],
    'sku': ['sku', 'item', 'product', 'medicine'],
    'revenue': ['revenue', 'sales', 'issue_value', 'issue value'],
    'issue_qty': ['issue_qty', 'issue qty', 'sold_qty', 'quantity sold'],
    'closing_qty': ['closing_qty', 'closing qty', 'stock', 'closing stock'],
    'date': ['date', 'txn_date', 'invoice_date', 'day'],
}


def _normalize(value: str) -> str:
    return ''.join(ch.lower() for ch in str(value) if ch.isalnum())


def map_columns(headers: List[str]) -> Dict[str, str]:
    norm_headers = {header: _normalize(header) for header in headers}
    result: Dict[str, str] = {}
    for canonical, aliases in ALIASES.items():
        alias_set = {_normalize(a) for a in aliases}
        for raw, normalized in norm_headers.items():
            if normalized in alias_set:
                result[canonical] = raw
                break
    return result


def missing_required(mapping: Dict[str, str]) -> List[str]:
    required = ['category', 'sku', 'revenue', 'issue_qty', 'closing_qty']
    return [item for item in required if item not in mapping]
