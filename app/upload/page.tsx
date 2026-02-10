'use client';

import { useState } from 'react';
import Papa from 'papaparse';

const STORAGE_KEY = 'kareema-personal-data';

export default function UploadPage() {
  const [message, setMessage] = useState('');
  return (
    <div className="grid">
      <h1>Upload CSV (Personal Mode)</h1>
      <div className="card">
        <input type="file" accept=".csv" onChange={(e) => {
          const file = e.target.files?.[0];
          if (!file) return;
          Papa.parse(file, { header: true, skipEmptyLines: true, complete: (result) => {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(result.data));
            setMessage(`Saved ${result.data.length} rows to browser storage.`);
          }});
        }} />
        <p className="muted">Upload your own inventory export and it will power Personal Mode on dashboard/charts/models.</p>
        {!!message && <p>{message}</p>}
      </div>
    </div>
  );
}
