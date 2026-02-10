export default function AboutPage() {
  return (
    <div className="grid">
      <h1>About & Methodology</h1>
      <div className="card">
        <p>This app operationalizes the IITM BDM capstone into live analytics for Kareema Medical Store.</p>
        <ul>
          <li>Demand and revenue concentration by therapeutic category (Pareto + ABC).</li>
          <li>Stockout risk scoring from issue vs closing quantity.</li>
          <li>Forecasting via ARIMA/SARIMA with model diagnostics (MAPE + ADF).</li>
          <li>Demo Mode uses repository dataset; Personal Mode uses uploaded CSV + daily entries in browser storage.</li>
        </ul>
      </div>
    </div>
  );
}
