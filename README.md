# Kareema Medical Store Live Analytics

Production-ready Next.js + Python serverless analytics app for interactive pharmacy insights.

## Features
- **Demo Mode**: loads repository dataset from `data/`.
- **Personal Mode**: upload CSV and append daily entries (stored in browser `localStorage`).
- Interactive Plotly dashboards:
  - Pareto revenue distribution
  - ABC classification
  - Stockout risk heatmap
  - Weekly/monthly trends
  - Forecast visualization (ARIMA/SARIMA)
  - Category comparison view
- Python analytics APIs for on-demand analysis and forecasting.

## Tech Stack
- Frontend: Next.js 14 (App Router), TypeScript, react-plotly.js
- Backend APIs: Python serverless functions (Vercel)
- Analytics: pandas, numpy, statsmodels, plotly

## Project Structure
- `app/` – Next.js pages (`/`, `/upload`, `/entry`, `/charts`, `/models`, `/reports`, `/about`)
- `components/` – reusable cards/tables/charts
- `analysis/` – reusable Python analytics modules
- `api/` – Python serverless endpoints
- `data/` – demo data source
- `tests/` – core mapping tests

## API Endpoints
- `POST /api/analyze` -> KPIs, tables, chart-ready Plotly JSON
- `POST /api/forecast` -> forecast points, confidence intervals, MAPE/ADF stats, Plotly JSON
- `POST /api/ai_summary` -> executive summary + risks + recommendations
- `POST /api/columns` -> header mapping and missing required columns

## Run Locally
1. Install Node deps:
   ```bash
   npm install
   ```
2. Run app:
   ```bash
   npm run dev
   ```
3. (Optional) Run tests:
   ```bash
   npm test
   ```

> Note: Python endpoints (`/api/*.py`) are executed on Vercel Python runtime. Local `next dev` validates the frontend shell and routing; deploy to test Python functions end-to-end.

## Deploy on Vercel
1. Push this repo to GitHub.
2. Import project in Vercel.
3. Vercel will detect Next.js and `vercel.json` Python functions.
4. Deploy.

## Data Notes
- Demo dataset: `data/KAREEMA MEDICAL STORE  - Sales_Data.csv`
- Supports CSV upload with flexible column aliases (`Therapeutic Tag`, `Revenue`, `ISSUE_QTY`, `CLOSING_QTY`, etc.)
- Use **Reset to Demo Data** on dashboard to return to baseline dataset.

## Binary Files Policy (for PR compatibility)
To avoid PR creation failures on platforms that reject binary files in diffs:
- **Do not add PDFs/images under `public/`**.
- Keep project documents in **`report/`** (source reports) and serve them via `app/report/[file]/route.ts`.
- Keep static reference charts in **`charts/`** only if they already exist in the base branch.
- For new uploads, store user data as CSV/JSON only (no binary upload persistence in git).

If you need to add new reports manually, place them in:
- `report/<your-file>.pdf`

The app automatically lists these files on `/reports` and serves them from `/report/<filename>`.
