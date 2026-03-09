from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.scoring_service import calculate_stock_score, calculate_health_check

router = APIRouter()

@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    result = []
    
    # Calculate sector sums for stock weighting later, but first we need all scores
    scores = {}
    sector_sums = {
        "AI & Cloud": 0, "Semiconductors": 0, "Clean Energy": 0, 
        "EV & Battery": 0, "Biotech": 0, "Defense": 0
    }
    
    for c in companies:
        score_data = calculate_stock_score(c.metrics)
        scores[c.id] = score_data
        if c.sector in sector_sums:
            sector_sums[c.sector] += score_data["total_score"]
            
    for c in companies:
        c_score = scores[c.id]
        health = calculate_health_check(c.metrics)
        
        # Calculate sector weight
        sec_sum = sector_sums.get(c.sector, 1)
        if sec_sum == 0:
            sec_sum = 1
        sector_weight = round((c_score["total_score"] / sec_sum) * 100, 2)
        
        result.append({
            "id": c.id,
            "name": c.name,
            "symbol": c.symbol,
            "sector": c.sector,
            "metrics": {
                "revenue_cagr": c.metrics.revenue_cagr if c.metrics else 0,
                "pat_cagr": c.metrics.pat_cagr if c.metrics else 0,
                "roe": c.metrics.roe if c.metrics else 0,
                "roce": c.metrics.roce if c.metrics else 0,
                "debt_to_equity": c.metrics.debt_to_equity if c.metrics else 0,
                "market_cap_crs": c.metrics.market_cap_crs if c.metrics else 0
            },
            "score": c_score,
            "health": health,
            "sector_weight": sector_weight
        })
        
    return result
