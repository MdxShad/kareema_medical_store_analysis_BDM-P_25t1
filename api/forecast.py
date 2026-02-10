from __future__ import annotations
from analysis.forecasting import run_forecast
from api._utils import parse_request_json, load_dataframe_from_payload, response


def handler(request):
    try:
        payload = parse_request_json(request)
        df = load_dataframe_from_payload(payload, request=request)
        model = payload.get('model', 'ARIMA')
        result = run_forecast(df, model=model)
        return response(result, 200)
    except Exception as exc:
        return response({'error': str(exc)}, 400)
