const aliases: Record<string, string[]> = {
  category: ['therapeutic tag', 'category', 'class', 'segment'],
  sku: ['sku', 'item', 'product', 'medicine'],
  revenue: ['revenue', 'sales', 'issue_value', 'issue value'],
  issue_qty: ['issue_qty', 'issue qty', 'sold_qty', 'quantity sold'],
  closing_qty: ['closing_qty', 'closing qty', 'stock', 'closing stock'],
  date: ['date', 'txn_date', 'invoice_date', 'day'],
};

const normalize = (value: string) => value.toLowerCase().replace(/[^a-z0-9]/g, '');

export function mapColumns(headers: string[]) {
  const normalized = headers.map((h) => ({ raw: h, key: normalize(h) }));
  const result: Record<string, string> = {};
  for (const [canonical, values] of Object.entries(aliases)) {
    const candidates = values.map(normalize);
    const found = normalized.find((h) => candidates.includes(h.key));
    if (found) result[canonical] = found.raw;
  }
  return result;
}

export function getMissingRequiredColumns(mapping: Record<string, string>) {
  return ['category', 'sku', 'revenue', 'issue_qty', 'closing_qty'].filter((key) => !mapping[key]);
}
