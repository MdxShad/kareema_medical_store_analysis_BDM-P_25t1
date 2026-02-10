'use client';

import { useState } from 'react';

const STORAGE_KEY = 'kareema-personal-data';
const initial = { Date: '', SKU: '', 'Therapeutic Tag': '', ISSUE_QTY: '', CLOSING_QTY: '', Revenue: '' };

export default function EntryPage() {
  const [form, setForm] = useState(initial);
  const [msg, setMsg] = useState('');
  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const rows = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    rows.push(form);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(rows));
    setMsg('Daily entry appended to Personal Mode dataset.');
    setForm(initial);
  };
  const download = () => {
    const rows = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    if (!rows.length) return;
    const headers = Object.keys(rows[0]);
    const csv = [headers.join(','), ...rows.map((r: any) => headers.map((h) => JSON.stringify(r[h] ?? '')).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'kareema_personal_data.csv'; a.click(); URL.revokeObjectURL(url);
  };
  return (
    <div className="grid">
      <h1>Daily Entry</h1>
      <form className="card grid" onSubmit={onSubmit}>
        {Object.entries(form).map(([k,v]) => <label key={k}>{k}<input value={v} onChange={(e)=>setForm((s)=>({...s,[k]:e.target.value}))} required /></label>)}
        <div className="controls"><button type="submit">Append Entry</button><button type="button" className="secondary" onClick={download}>Download Updated CSV</button></div>
        {msg && <p>{msg}</p>}
      </form>
    </div>
  );
}
