from __future__ import annotations
import json
from typing import Any, Dict
import pandas as pd
from analysis.data_loader import load_demo_data, load_csv_bytes


def parse_request_json(request) -> Dict[str, Any]:
    if hasattr(request, 'get_json'):
        data = request.get_json(silent=True)
        if data is not None:
            return data
    body = getattr(request, 'data', None)
    if body:
        return json.loads(body.decode('utf-8'))
    return {}


def _load_from_file(request):
    files = getattr(request, 'files', None)
    if not files:
        return None
    file = files.get('file') if hasattr(files, 'get') else None
    if file and hasattr(file, 'read'):
        return load_csv_bytes(file.read())
    return None


def load_dataframe_from_payload(payload: Dict[str, Any], request=None) -> pd.DataFrame:
    if request is not None:
        uploaded = _load_from_file(request)
        if uploaded is not None:
            return uploaded

    mode = payload.get('mode', 'demo')
    rows = payload.get('rows') or []
    if mode == 'personal' and rows:
        return pd.DataFrame(rows)
    return load_demo_data()


def response(data: Dict[str, Any], status: int = 200):
    return json.dumps(data), status, {'Content-Type': 'application/json'}
