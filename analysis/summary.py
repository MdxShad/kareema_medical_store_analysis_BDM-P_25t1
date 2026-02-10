from __future__ import annotations

def build_summary(payload: dict) -> dict:
    kpis = payload.get('kpis', {})
    findings = payload.get('key_findings', [])
    anomalies = payload.get('detected_anomalies', [])

    bullets = [
        f"Revenue snapshot: {kpis.get('Total Revenue', 'N/A')} with {kpis.get('SKU Count', 'N/A')} active SKUs.",
        "Top therapeutic categories should be protected with stricter reorder rules.",
    ]
    bullets.extend([f"Finding: {item}" for item in findings[:5]])
    bullets.extend([f"Risk: {item}" for item in anomalies[:5]])

    recommendations = [
        "Increase safety stock for A-class categories with high stockout risk.",
        "Set weekly monitoring on categories with rising cumulative contribution.",
        "Review slow-moving C-class SKUs and optimize purchase frequency.",
    ]

    return {
      'executive_summary': 'Kareema Medical Store analytics indicate concentrated revenue and targeted stockout risk that can be addressed by ABC-driven replenishment.',
      'risks': bullets,
      'recommendations': recommendations,
    }
