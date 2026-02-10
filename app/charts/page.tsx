'use client';
import { useEffect, useState } from 'react';
import { PlotCard } from '@/components/PlotCard';

export default function ChartsPage() {
  const [charts, setCharts] = useState<Record<string, any>>({});
  useEffect(() => { fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode: localStorage.getItem('kareema-personal-data') ? 'personal' : 'demo', rows: JSON.parse(localStorage.getItem('kareema-personal-data') || '[]') }) }).then(r => r.json()).then(j => setCharts(j.charts)); }, []);
  return <div className="grid"><h1>Charts Gallery</h1>{Object.entries(charts).map(([k,v]) => <PlotCard key={k} title={k} figure={v as any} />)}</div>;
}
