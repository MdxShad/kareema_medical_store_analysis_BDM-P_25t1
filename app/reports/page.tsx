import fs from 'node:fs';
import path from 'node:path';

export default function ReportsPage() {
  const reportDir = path.join(process.cwd(), 'report');
  const files = fs.existsSync(reportDir) ? fs.readdirSync(reportDir).filter((f) => f.toLowerCase().endsWith('.pdf')) : [];
  return (
    <div className="grid">
      <h1>Reports</h1>
      <div className="card">
        <ul>{files.map((f) => <li key={f}><a href={`/report/${encodeURIComponent(f)}`} target="_blank">{f}</a></li>)}</ul>
      </div>
    </div>
  );
}
