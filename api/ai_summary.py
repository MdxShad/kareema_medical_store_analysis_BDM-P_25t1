from __future__ import annotations
from analysis.summary import build_summary
from api._utils import parse_request_json, response


def handler(request):
    try:
        payload = parse_request_json(request)
        return response(build_summary(payload), 200)
    except Exception as exc:
        return response({'error': str(exc)}, 400)
