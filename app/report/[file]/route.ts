import { NextRequest } from 'next/server';
import fs from 'node:fs';
import path from 'node:path';

export async function GET(_: NextRequest, { params }: { params: { file: string } }) {
  const decoded = decodeURIComponent(params.file);
  const root = path.resolve(process.cwd(), 'report');
  const target = path.resolve(root, decoded);

  if (!target.startsWith(root) || !target.toLowerCase().endsWith('.pdf') || !fs.existsSync(target)) {
    return new Response('Report not found', { status: 404 });
  }

  const data = await fs.promises.readFile(target);
  return new Response(data, {
    status: 200,
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': `inline; filename="${path.basename(target)}"`,
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
