from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.scoring_service import calculate_stock_score
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import math

router = APIRouter()

SECTOR_ALLOCATIONS = {
    "AI & Cloud": 0.25,
    "Semiconductors": 0.20,
    "Clean Energy": 0.20,
    "EV & Battery": 0.15,
    "Biotech": 0.12,
    "Defense": 0.08
}

def get_stock_weights(companies):
    """Calculates the final mathematical index weight for each stock."""
    sector_sums = {
        "AI & Cloud": 0, "Semiconductors": 0, "Clean Energy": 0, 
        "EV & Battery": 0, "Biotech": 0, "Defense": 0
    }
    
    scores = {}
    for c in companies:
        score_data = calculate_stock_score(c.metrics)
        scores[c.id] = score_data["total_score"]
        sector_sums[c.sector] += score_data["total_score"]
        
    weights = {}
    for c in companies:
        sec_sum = sector_sums.get(c.sector, 1) or 1
        stock_sector_weight = scores[c.id] / sec_sum
        final_weight = SECTOR_ALLOCATIONS.get(c.sector, 0) * stock_sector_weight
        weights[c.symbol] = final_weight
        
    return weights

@router.get("/overview")
def get_index_overview(db: Session = Depends(get_db)):
    try:
        # Fetch the last 2 days of cached data
        recent_cache = db.query(models.CachedIndex).order_by(models.CachedIndex.date.desc()).limit(2).all()
        
        if len(recent_cache) >= 2:
            today_val = recent_cache[0].index_value
            yesterday_val = recent_cache[1].index_value
            percent_change = ((today_val - yesterday_val) / yesterday_val * 100) if yesterday_val > 0 else 0
        elif len(recent_cache) == 1:
            today_val = recent_cache[0].index_value
            percent_change = 0.0
        else:
            today_val = 1000.0
            percent_change = 0.0
            
        return {
            "index_value": round(today_val, 2),
            "percent_change": round(percent_change, 2),
            "allocations": [{"name": k, "value": v * 100} for k, v in SECTOR_ALLOCATIONS.items()]
        }
    except Exception as e:
        print("Error fetching cached index overview:", e)
        return {
            "index_value": 1000.00,
            "percent_change": 0.0,
            "allocations": [{"name": k, "value": v * 100} for k, v in SECTOR_ALLOCATIONS.items()]
        }

@router.get("/history")
def get_index_history(days: int = Query(30), db: Session = Depends(get_db)):
    try:
        cached_data = db.query(models.CachedIndex).order_by(models.CachedIndex.date.desc()).limit(days).all()
        # Reverse to get chronological order
        cached_data.reverse()
        
        history = []
        for entry in cached_data:
            history.append({
                "date": str(entry.date),
                "future_india": round(entry.index_value, 2),
                "nifty_50": round(entry.nifty_value, 2)
            })
            
        # Calculate real outperformance
        if len(history) >= 2:
            nifty_start = history[0]["nifty_50"]
            nifty_end = history[-1]["nifty_50"]
            nifty_perf = ((nifty_end - nifty_start) / nifty_start) * 100 if nifty_start > 0 else 0
            
            fi_start = history[0]["future_india"]
            fi_end = history[-1]["future_india"]
            fi_perf = ((fi_end - fi_start) / fi_start) * 100 if fi_start > 0 else 0
            
            outperformance = fi_perf - nifty_perf
        else:
            outperformance = 0
            
        return {
            "history": history,
            "outperformance": round(outperformance, 2)
        }
        
    except Exception as e:
        print("Error serving cached history:", e)
        return {"history": [], "outperformance": 0}
