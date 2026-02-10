from __future__ import annotations
from analysis.analytics import run_analysis
from api._utils import parse_request_json, load_dataframe_from_payload, response


def handler(request):
    try:
        payload = parse_request_json(request)
        df = load_dataframe_from_payload(payload, request=request)
        result = run_analysis(df)
        result['mode'] = payload.get('mode', 'demo')
        return response(result, 200)
    except Exception as exc:
        return response({'error': str(exc)}, 400)
