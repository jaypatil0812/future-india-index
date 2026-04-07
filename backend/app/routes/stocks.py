from fastapi import APIRouter, Query
from app.services.stock_service import fetch_and_store_stock_by_name
import yfinance as yf

router = APIRouter()

@router.get("/company/{company_name}")
def get_stock_by_name(company_name: str, days: int = Query(30, description="Number of days of stock data")):
    """
    Fetch and store stock data for the given company name.
    Optional query parameter 'days' limits the number of days returned.
    """
    return fetch_and_store_stock_by_name(company_name, days)

@router.get("/company/{company_name}/info")
def get_company_info(company_name: str):
    """
    Fetch company brief information using yfinance.
    """
    try:
        ticker = yf.Ticker(company_name)
        info = ticker.info
        return {
            "summary": info.get("longBusinessSummary", "No brief available."),
            "industry": info.get("industry", "Unknown"),
            "website": info.get("website", "")
        }
    except Exception as e:
        return {"error": str(e), "summary": "Failed to load company brief from Yahoo Finance."}
