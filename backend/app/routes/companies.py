from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.scoring_service import calculate_stock_score, calculate_health_check

router = APIRouter()

SECTOR_ALLOCATIONS = {
    "AI & Cloud": 0.25,
    "Semiconductors": 0.20,
    "Clean Energy": 0.20,
    "EV & Battery": 0.15,
    "Biotech": 0.12,
    "Defense": 0.08
}

@router.get("")
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    try:
        companies = db.query(models.Company).all()
        
        if not companies:
            return []
        
        # Calculate sector sums for stock weighting
        scores = {}
        sector_sums = {k: 0 for k in SECTOR_ALLOCATIONS}
        
        for c in companies:
            if c.metrics:
                score_data = calculate_stock_score(c.metrics)
            else:
                score_data = {"total_score": 50.0, "growth": 0, "profitability": 0, "quality": 0, "innovation": 0, "scale": 0}
            scores[c.id] = score_data
            if c.sector in sector_sums:
                sector_sums[c.sector] += score_data["total_score"]
                
        result = []
        for c in companies:
            try:
                c_score = scores[c.id]
                health = calculate_health_check(c.metrics) if c.metrics else []
                
                sec_sum = sector_sums.get(c.sector, 1) or 1
                sector_alloc = SECTOR_ALLOCATIONS.get(c.sector, 0)
                sector_weight = round((c_score["total_score"] / sec_sum) * sector_alloc * 100, 2)
                
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
            except Exception as inner_e:
                print(f"Error processing company {c.name}: {inner_e}")
                continue
                
        return result
    
    except Exception as e:
        print(f"Error in /companies: {e}")
        return []
