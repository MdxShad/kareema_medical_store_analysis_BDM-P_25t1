export type DataRow = Record<string, string | number | null>;

export type AnalyzeResponse = {
  mode: 'demo' | 'personal';
  resolvedColumns: Record<string, string>;
  kpis: Record<string, number>;
  tables: {
    topProducts: Array<Record<string, string | number>>;
    categorySummary: Array<Record<string, string | number>>;
  };
  charts: Record<string, { data: any[]; layout: any }>;
  warnings: string[];
};
