import yfinance as yf
from app.models import SessionLocal, Company, CachedIndex
from app.services.scoring_service import calculate_stock_score
import pandas as pd
import math
from datetime import datetime, timedelta

SECTOR_ALLOCATIONS = {
    "AI & Cloud": 0.25,
    "Semiconductors": 0.20,
    "Clean Energy": 0.20,
    "EV & Battery": 0.15,
    "Biotech": 0.12,
    "Defense": 0.08
}

def get_stock_weights(companies):
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
        stock_sec_w = scores[c.id] / sec_sum
        weights[c.symbol] = SECTOR_ALLOCATIONS.get(c.sector, 0) * stock_sec_w
    return weights

def update_index_cache():
    """Background task to fetch yfinance data and update the cached index values."""
    print("Executing background cache update...")
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        if not companies:
            return
            
        weights = get_stock_weights(companies)
        symbols = [c.symbol for c in companies]
        
        # Download 400 days to ensure 1 Year of historical trading data
        index_data = yf.download(symbols, period="400d", interval="1d", progress=False)
        nifty_data = yf.download("^NSEI", period="400d", interval="1d", progress=False)
        
        try:
            if isinstance(nifty_data["Close"], type(nifty_data)) and "^NSEI" in nifty_data["Close"]:
                nifty_series = nifty_data["Close"]["^NSEI"].dropna()
            else:
                nifty_series = nifty_data["Close"].dropna()
        except:
            nifty_series = nifty_data["Close"].dropna()
            
        if len(symbols) > 1:
            index_closes = index_data["Close"].dropna(how='all')
        else:
            index_closes = index_data["Close"].dropna()
            
        # Clear old cache to prevent unlimited DB bloat
        db.query(CachedIndex).delete()
        
        # Recalculate and insert the entire known history (up to 400 days)
        for date in nifty_series.index:
            if date in index_closes.index:
                daily_index_val = 0
                for symbol, weight in weights.items():
                    try:
                        if len(symbols) > 1:
                            price = float(index_closes.loc[date, symbol])
                        else:
                            price = float(index_closes.loc[date])
                        if math.isnan(price): price = 100.0
                    except:
                        price = 100.0
                        
                    daily_index_val += price * (weight * 10)
                
                nifty_price = float(nifty_series.loc[date])
                
                # Check for existing
                exists = db.query(CachedIndex).filter(CachedIndex.date == date.date()).first()
                if not exists:
                    new_entry = CachedIndex(
                        date=date.date(),
                        index_value=daily_index_val,
                        nifty_value=nifty_price
                    )
                    db.add(new_entry)
        
        db.commit()
        
        # 2. Update individual StockPrice caches using the same downloaded dataset
        from app.models import StockPrice
        
        # Clear old stock histories to prevent db bloat
        db.query(StockPrice).delete()
        
        for c in companies:
            sym = c.symbol
            try:
                # Iterate over the 400 days we just downloaded
                for date in index_data.index:
                    def get_val(col):
                        if len(symbols) > 1:
                            v = index_data[col][sym].loc[date]
                        else:
                            v = index_data[col].loc[date]
                        return float(v) if not pd.isna(v) else 0.0

                    close_p = get_val("Close")
                    if close_p > 0: # Only save valid trading days
                        sp = StockPrice(
                            company_id=c.id,
                            date=date.date(),
                            open=get_val("Open"),
                            close=close_p,
                            high=get_val("High"),
                            low=get_val("Low"),
                            volume=get_val("Volume")
                        )
                        db.add(sp)
            except Exception as e:
                print(f"Error caching inner stock {sym}: {e}")
                
        db.commit()
        print("Successfully updated Future India Index cache.")
        
    except Exception as e:
        db.rollback()
        print(f"Error updating cache: {e}")
    finally:
        db.close()
