export function DataTable({ rows, title }: { rows: Array<Record<string, string | number>>; title: string }) {
  if (!rows?.length) return null;
  const headers = Object.keys(rows[0]);
  return (
    <div className="card">
      <h3>{title}</h3>
      <table>
        <thead><tr>{headers.map((h) => <th key={h}>{h}</th>)}</tr></thead>
        <tbody>
          {rows.map((row, idx) => <tr key={idx}>{headers.map((h) => <td key={h}>{String(row[h] ?? '')}</td>)}</tr>)}
        </tbody>
      </table>
    </div>
  );
}
