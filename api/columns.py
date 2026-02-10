from __future__ import annotations
from analysis.mapping import map_columns, missing_required
from api._utils import parse_request_json, response


def handler(request):
    try:
        payload = parse_request_json(request)
        headers = payload.get('headers', [])
        mapped = map_columns(headers)
        return response({'mapping': mapped, 'missing': missing_required(mapped)}, 200)
    except Exception as exc:
        return response({'error': str(exc)}, 400)
