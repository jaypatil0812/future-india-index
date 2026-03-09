import math

def calculate_stock_score(metrics):
    if not metrics:
        return {"total_score": 0, "components": {}}

    # 1. Growth Score (Capped at 100)
    rev_score = min(metrics.revenue_cagr, 50.0) if metrics.revenue_cagr > 0 else 0
    pat_score = min(metrics.pat_cagr, 50.0) if metrics.pat_cagr > 0 else 0
    growth_score = rev_score + pat_score

    # 2. Profitability Score (Capped at 100)
    roe_score = min(metrics.roe, 40.0) if metrics.roe > 0 else 0
    roce_score = min(metrics.roce, 30.0) if metrics.roce > 0 else 0
    margin_score = min(metrics.operating_margin, 30.0) if metrics.operating_margin > 0 else 0
    profit_score = roe_score + roce_score + margin_score
    
    # 3. Quality Score (Max 100)
    de = metrics.debt_to_equity
    if de <= 0.3: de_score = 40
    elif de <= 0.6: de_score = 30
    elif de <= 1.0: de_score = 20
    else: de_score = 0

    ic = metrics.interest_coverage
    if ic >= 10: ic_score = 30
    elif ic >= 5: ic_score = 20
    elif ic >= 2: ic_score = 10
    else: ic_score = 0

    cr = metrics.current_ratio
    if cr >= 1.5: cr_score = 30
    elif cr >= 1.2: cr_score = 20
    elif cr >= 1.0: cr_score = 10
    else: cr_score = 0
    
    quality_score = de_score + ic_score + cr_score

    # 4. Innovation Score (Max 100)
    rd_score = min((metrics.rd_percent / 10.0) * 60, 60.0) if metrics.rd_percent > 0 else 0
    innovation_score = rd_score + getattr(metrics, 'product_pipeline_score', 0)

    # 5. Scale Score (Max 100)
    mc = max(metrics.market_cap_crs, 1)
    scale_score = min((math.log10(mc) / math.log10(100000)) * 100, 100.0)

    # Final Stock Score Calculation
    total_score = round(
        (0.25 * growth_score) +
        (0.25 * profit_score) +
        (0.20 * quality_score) +
        (0.15 * innovation_score) +
        (0.15 * scale_score), 1
    )

    return {
        "total_score": total_score,
        "components": {
            "growth": round(growth_score, 1),
            "profitability": round(profit_score, 1),
            "quality": round(quality_score, 1),
            "innovation": round(innovation_score, 1),
            "scale": round(scale_score, 1)
        }
    }

def calculate_health_check(metrics):
    if not metrics:
        return {"status": "red", "criteria": []}

    criteria = [
        {"name": "ROE ≥ 15%", "passed": metrics.roe >= 15},
        {"name": "ROCE ≥ 12%", "passed": metrics.roce >= 12},
        {"name": "Debt/Equity ≤ 1.0", "passed": metrics.debt_to_equity <= 1.0},
        {"name": "Revenue CAGR ≥ 15%", "passed": metrics.revenue_cagr >= 15}
    ]

    passed_count = sum(1 for c in criteria if c["passed"])
    
    if passed_count == 4:
        status = "green"
    elif passed_count >= 2:
        status = "yellow"
    else:
        status = "red"

    return {
        "status": status,
        "criteria": criteria
    }
