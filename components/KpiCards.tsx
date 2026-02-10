export function KpiCards({ kpis }: { kpis: Record<string, number> }) {
  return (
    <div className="grid kpi-grid">
      {Object.entries(kpis).map(([label, value]) => (
        <div className="card" key={label}>
          <div className="muted">{label}</div>
          <div className="kpi-value">{Number(value).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</div>
        </div>
      ))}
    </div>
  );
}
