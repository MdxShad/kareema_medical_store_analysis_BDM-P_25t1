'use client';

import { useEffect, useMemo, useState } from 'react';
import { KpiCards } from './KpiCards';
import { PlotCard } from './PlotCard';
import { DataTable } from './DataTable';
import type { AnalyzeResponse, DataRow } from '@/lib/types';

const STORAGE_KEY = 'kareema-personal-data';

export function DashboardClient() {
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState('all');

  const loadData = async (mode: 'demo' | 'personal') => {
    setLoading(true); setError(null);
    try {
      const personalRows: DataRow[] = mode === 'personal' ? JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') : [];
      const resp = await fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode, rows: personalRows }) });
      if (!resp.ok) throw new Error(await resp.text());
      const json = await resp.json();
      setAnalysis(json);
    } catch (e) { setError((e as Error).message); }
    finally { setLoading(false); }
  };

  useEffect(() => { void loadData(localStorage.getItem(STORAGE_KEY) ? 'personal' : 'demo'); }, []);

  const filteredTable = useMemo(() => {
    if (!analysis) return [];
    if (category === 'all') return analysis.tables.topProducts;
    return analysis.tables.topProducts.filter((r) => String(r.Category) === category);
  }, [analysis, category]);

  const categories = useMemo(() => ['all', ...new Set((analysis?.tables.categorySummary || []).map((x) => String(x.Category)))], [analysis]);

  return (
    <div className="grid" style={{ gap: 18 }}>
      <h1>Kareema Medical Store Live Analytics</h1>
      <div className="controls">
        <button onClick={() => loadData('demo')}>Demo Mode</button>
        <button className="secondary" onClick={() => loadData('personal')}>Personal Mode</button>
        <button onClick={() => { localStorage.removeItem(STORAGE_KEY); void loadData('demo'); }}>Reset to Demo Data</button>
        <select value={category} onChange={(e) => setCategory(e.target.value)}>{categories.map((c) => <option key={c}>{c}</option>)}</select>
      </div>
      {loading && <div className="card">Loading analytics…</div>}
      {error && <div className="card">Error: {error}</div>}
      {analysis && (
        <>
          <KpiCards kpis={analysis.kpis} />
          <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
            {Object.entries(analysis.charts).slice(0, 4).map(([k, fig]) => <PlotCard key={k} title={k} figure={fig} />)}
          </div>
          <DataTable title="Top Products" rows={filteredTable} />
          <DataTable title="Category Summary" rows={analysis.tables.categorySummary} />
        </>
      )}
    </div>
  );
}
