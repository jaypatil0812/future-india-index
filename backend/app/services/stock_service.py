from app.models import SessionLocal, Company, StockPrice
import pandas as pd

def fetch_and_store_stock_by_name(company_name: str, days: int = 30):
    db = SessionLocal()
    try:
        company = db.query(Company).filter(
            (Company.symbol.ilike(company_name)) | (Company.name.ilike(company_name))
        ).first()
        
        if not company:
            return {"error": "Company not found"}
            
        # Fetch directly from the background-populated cache table
        cached_prices = db.query(StockPrice)\
            .filter(StockPrice.company_id == company.id)\
            .order_by(StockPrice.date.desc())\
            .limit(days)\
            .all()
            
        # The frontend chart expects them chronologically (oldest to newest)
        cached_prices.reverse()
        
        response = []
        for sp in cached_prices:
            response.append({
                "date": str(sp.date),
                "open": round(sp.open, 2),
                "close": round(sp.close, 2),
                "high": round(sp.high, 2),
                "low": round(sp.low, 2),
                "volume": int(sp.volume)
            })
            
        return response
    except Exception as e:
        print(f"Error serving cached individual stock data for {company_name}: {e}")
        return []
    finally:
        db.close()
