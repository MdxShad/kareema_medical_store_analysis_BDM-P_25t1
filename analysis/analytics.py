from __future__ import annotations
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from .mapping import map_columns, missing_required


def _to_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors='coerce').fillna(0)


def run_analysis(df: pd.DataFrame):
    mapping = map_columns(list(df.columns))
    missing = missing_required(mapping)
    if missing:
        raise ValueError(f"Missing required columns after mapping: {', '.join(missing)}")

    category_col = mapping['category']
    sku_col = mapping['sku']
    revenue_col = mapping['revenue']
    issue_col = mapping['issue_qty']
    closing_col = mapping['closing_qty']
    date_col = mapping.get('date')

    work = df.copy()
    work[revenue_col] = _to_num(work[revenue_col])
    work[issue_col] = _to_num(work[issue_col])
    work[closing_col] = _to_num(work[closing_col])

    cat = work.groupby(category_col, as_index=False)[revenue_col].sum().sort_values(revenue_col, ascending=False)
    cat['pct'] = (cat[revenue_col] / cat[revenue_col].sum() * 100).round(2)
    cat['cum_pct'] = cat['pct'].cumsum().round(2)

    abc = cat.copy()
    abc['class'] = np.where(abc['cum_pct'] <= 80, 'A', np.where(abc['cum_pct'] <= 95, 'B', 'C'))

    work['risk_score'] = np.where(work[closing_col] < 0, 3, np.where(work[closing_col] < work[issue_col] * 0.1, 2, np.where(work[closing_col] < work[issue_col] * 0.3, 1, 0)))
    risk_table = work.groupby(category_col, as_index=False)['risk_score'].mean().sort_values('risk_score', ascending=False)

    top_products = work[[sku_col, category_col, revenue_col, issue_col, closing_col]].sort_values(revenue_col, ascending=False).head(20)
    top_products.columns = ['SKU', 'Category', 'Revenue', 'Issue Qty', 'Closing Qty']

    kpis = {
        'Total Revenue': float(work[revenue_col].sum()),
        'Total Issue Qty': float(work[issue_col].sum()),
        'Total Closing Qty': float(work[closing_col].sum()),
        'SKU Count': float(work[sku_col].nunique()),
        'Category Count': float(work[category_col].nunique()),
    }

    trend = None
    if date_col and date_col in work.columns:
      temp = work[[date_col, revenue_col]].copy()
      temp[date_col] = pd.to_datetime(temp[date_col], errors='coerce')
      temp = temp.dropna(subset=[date_col])
      if not temp.empty:
        weekly = temp.set_index(date_col).resample('W')[revenue_col].sum()
        monthly = temp.set_index(date_col).resample('M')[revenue_col].sum()
        trend = {
          'weekly': go.Figure(data=[go.Scatter(x=weekly.index.astype(str), y=weekly.values, mode='lines+markers')], layout={'title': 'Weekly Revenue Trend'}).to_plotly_json(),
          'monthly': go.Figure(data=[go.Bar(x=monthly.index.astype(str), y=monthly.values)], layout={'title': 'Monthly Revenue Trend'}).to_plotly_json(),
        }

    charts = {
        'Pareto Revenue Distribution': go.Figure(data=[
            go.Bar(x=cat[category_col], y=cat[revenue_col], name='Revenue'),
            go.Scatter(x=cat[category_col], y=cat['cum_pct'], name='Cumulative %', yaxis='y2', mode='lines+markers')
        ], layout={'title': 'Pareto Revenue Distribution', 'yaxis2': {'overlaying': 'y', 'side': 'right', 'range': [0, 100]}}).to_plotly_json(),
        'ABC Classification': go.Figure(data=[go.Bar(x=abc[category_col], y=abc[revenue_col], marker={'color': abc['class'].map({'A':'#ef4444','B':'#f59e0b','C':'#10b981'})})], layout={'title': 'ABC Classification'}).to_plotly_json(),
        'Stockout Risk Heatmap': go.Figure(data=[go.Heatmap(z=[risk_table['risk_score'].tolist()], x=risk_table[category_col].tolist(), y=['Risk'])], layout={'title': 'Stockout Risk Heatmap'}).to_plotly_json(),
        'Category Comparison Dashboard': go.Figure(data=[go.Bar(x=cat[category_col], y=cat['pct'])], layout={'title': 'Category Comparison (% Revenue)'}).to_plotly_json(),
    }
    if trend:
      charts['Weekly Trend'] = trend['weekly']
      charts['Monthly Trend'] = trend['monthly']

    return {
        'resolvedColumns': mapping,
        'kpis': kpis,
        'tables': {
            'topProducts': top_products.round(2).to_dict(orient='records'),
            'categorySummary': abc[[category_col, revenue_col, 'pct', 'cum_pct', 'class']].rename(columns={category_col: 'Category', revenue_col: 'Revenue', 'pct': 'Revenue %', 'cum_pct': 'Cumulative %', 'class': 'ABC Class'}).round(2).to_dict(orient='records'),
        },
        'charts': json.loads(json.dumps(charts, default=str)),
        'warnings': [],
    }
