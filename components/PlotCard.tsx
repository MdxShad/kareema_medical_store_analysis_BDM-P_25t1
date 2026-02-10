'use client';

import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export function PlotCard({ title, figure }: { title: string; figure: { data: any[]; layout: any } }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <Plot data={figure.data} layout={{ ...figure.layout, autosize: true }} style={{ width: '100%', height: 420 }} useResizeHandler />
    </div>
  );
}
