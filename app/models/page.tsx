'use client';

import { useState } from 'react';
import { PlotCard } from '@/components/PlotCard';

export default function ModelsPage() {
  const [data, setData] = useState<any>(null);
  const runForecast = async (model: 'ARIMA' | 'SARIMA') => {
    const res = await fetch('/api/forecast', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model, mode: localStorage.getItem('kareema-personal-data') ? 'personal' : 'demo', rows: JSON.parse(localStorage.getItem('kareema-personal-data') || '[]') }) });
    setData(await res.json());
  };
  return (
    <div className="grid">
      <h1>Forecasting + Metrics</h1>
      <div className="controls"><button onClick={() => runForecast('ARIMA')}>Run ARIMA</button><button className="secondary" onClick={() => runForecast('SARIMA')}>Run SARIMA</button></div>
      {data?.metrics && <div className="card">MAPE: {data.metrics.mape?.toFixed?.(2)} | ADF p-value: {data.metrics.adf_pvalue?.toFixed?.(4)} | Model: {data.model}</div>}
      {data?.plotly && <PlotCard title="Forecast" figure={data.plotly} />}
    </div>
  );
}
