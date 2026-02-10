from __future__ import annotations
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from .mapping import map_columns


def _build_time_series(df: pd.DataFrame, date_col: str | None, value_col: str) -> pd.Series:
    work = df.copy()
    work[value_col] = pd.to_numeric(work[value_col], errors='coerce').fillna(0)

    if date_col and date_col in work.columns:
        dated = work[[date_col, value_col]].copy()
        dated[date_col] = pd.to_datetime(dated[date_col], errors='coerce')
        dated = dated.dropna(subset=[date_col]).sort_values(date_col)
        if not dated.empty:
            return dated.set_index(date_col).resample('W')[value_col].sum()

    # Fallback for datasets without dates (demo CSV): generate synthetic weekly index.
    synthetic = work[[value_col]].copy().reset_index(drop=True)
    synthetic.index = pd.date_range(start='2024-01-07', periods=len(synthetic), freq='W')
    return synthetic[value_col]


def run_forecast(df: pd.DataFrame, model: str = 'ARIMA', periods: int = 8):
    mapping = map_columns(list(df.columns))
    value_col = mapping.get('revenue')
    if not value_col:
        raise ValueError('Revenue/sales column is required for forecasting.')

    ts = _build_time_series(df, mapping.get('date'), value_col)
    if len(ts) < 12:
        raise ValueError('Not enough records for forecasting. Add at least 12 rows.')

    if model.upper() == 'SARIMA':
        fitted = SARIMAX(ts, order=(1, 1, 1), seasonal_order=(1, 1, 1, 4)).fit(disp=False)
    else:
        fitted = ARIMA(ts, order=(2, 1, 2)).fit()

    pred = fitted.get_forecast(steps=periods)
    conf = pred.conf_int()
    forecast = pred.predicted_mean

    # Use in-sample one-step predictions for evaluation.
    fitted_vals = fitted.predict(start=1, end=len(ts) - 1)
    actual = ts.iloc[1:1 + len(fitted_vals)]
    mape = float(np.mean(np.abs((actual.values - fitted_vals.values) / np.maximum(actual.values, 1e-6))) * 100)

    adf_stat = adfuller(ts.values)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts.index.astype(str), y=ts.values, name='Observed', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=forecast.index.astype(str), y=forecast.values, name='Forecast', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=forecast.index.astype(str), y=conf.iloc[:, 0], mode='lines', line={'width': 0}, showlegend=False))
    fig.add_trace(go.Scatter(x=forecast.index.astype(str), y=conf.iloc[:, 1], mode='lines', fill='tonexty', name='95% CI', line={'width': 0}))
    fig.update_layout(title=f'{model.upper()} Forecast')

    return {
        'model': model.upper(),
        'forecast_points': [{'date': str(idx.date()), 'value': float(val)} for idx, val in forecast.items()],
        'confidence_intervals': [{'date': str(idx.date()), 'lower': float(low), 'upper': float(up)} for idx, (low, up) in zip(conf.index, conf.values)],
        'metrics': {'mape': mape, 'adf_stat': float(adf_stat[0]), 'adf_pvalue': float(adf_stat[1])},
        'plotly': json.loads(json.dumps(fig.to_plotly_json(), default=str)),
    }
