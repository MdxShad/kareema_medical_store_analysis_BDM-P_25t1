import './globals.css';
import Link from 'next/link';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav className="nav">
          <Link href="/">Dashboard</Link>
          <Link href="/upload">Upload CSV</Link>
          <Link href="/entry">Daily Entry</Link>
          <Link href="/charts">Charts</Link>
          <Link href="/models">Models</Link>
          <Link href="/reports">Reports</Link>
          <Link href="/about">About</Link>
        </nav>
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
