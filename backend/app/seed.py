import os
from app.models import SessionLocal, Base, engine, Company, CompanyMetrics

# Drop existing tables and recreate them to apply schema changes
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

india_companies = [
    # AI & Cloud (25%)
    {"name": "Infosys", "symbol": "INFY.NS", "sector": "AI & Cloud", "metrics": {"revenue_cagr": 12.0, "pat_cagr": 10.0, "roe": 31.0, "roce": 35.0, "operating_margin": 24.0, "debt_to_equity": 0.05, "interest_coverage": 150.0, "current_ratio": 2.2, "rd_percent": 3.0, "product_pipeline_score": 25, "market_cap_crs": 650000}},
    {"name": "Persistent Systems", "symbol": "PERSISTENT.NS", "sector": "AI & Cloud", "metrics": {"revenue_cagr": 20.0, "pat_cagr": 22.0, "roe": 26.0, "roce": 30.0, "operating_margin": 18.0, "debt_to_equity": 0.1, "interest_coverage": 85.0, "current_ratio": 2.5, "rd_percent": 3.5, "product_pipeline_score": 25, "market_cap_crs": 65000}},
    {"name": "L&T Technology Services", "symbol": "LTTS.NS", "sector": "AI & Cloud", "metrics": {"revenue_cagr": 16.0, "pat_cagr": 18.0, "roe": 28.0, "roce": 35.0, "operating_margin": 21.0, "debt_to_equity": 0.12, "interest_coverage": 90.0, "current_ratio": 2.8, "rd_percent": 4.5, "product_pipeline_score": 40, "market_cap_crs": 55000}},
    {"name": "Tata Elxsi", "symbol": "TATAELXSI.NS", "sector": "AI & Cloud", "metrics": {"revenue_cagr": 18.0, "pat_cagr": 20.0, "roe": 40.0, "roce": 45.0, "operating_margin": 29.0, "debt_to_equity": 0.02, "interest_coverage": 200.0, "current_ratio": 3.5, "rd_percent": 5.0, "product_pipeline_score": 40, "market_cap_crs": 45000}},
    {"name": "Coforge", "symbol": "COFORGE.NS", "sector": "AI & Cloud", "metrics": {"revenue_cagr": 18.0, "pat_cagr": 16.0, "roe": 25.0, "roce": 30.0, "operating_margin": 19.0, "debt_to_equity": 0.15, "interest_coverage": 65.0, "current_ratio": 2.1, "rd_percent": 3.0, "product_pipeline_score": 25, "market_cap_crs": 38000}},

    # Semiconductors (20%)
    {"name": "Tata Electronics (BEL partnership)", "symbol": "TATAELEC.NS", "sector": "Semiconductors", "metrics": {"revenue_cagr": 25.0, "pat_cagr": 20.0, "roe": 25.0, "roce": 22.0, "operating_margin": 15.0, "debt_to_equity": 0.4, "interest_coverage": 8.0, "current_ratio": 1.5, "rd_percent": 5.0, "product_pipeline_score": 40, "market_cap_crs": 50000}},
    {"name": "Kaynes Technology", "symbol": "KAYNES.NS", "sector": "Semiconductors", "metrics": {"revenue_cagr": 35.0, "pat_cagr": 40.0, "roe": 18.0, "roce": 20.0, "operating_margin": 14.0, "debt_to_equity": 0.4, "interest_coverage": 8.5, "current_ratio": 1.8, "rd_percent": 4.0, "product_pipeline_score": 25, "market_cap_crs": 18000}},
    {"name": "Dixon Technologies", "symbol": "DIXON.NS", "sector": "Semiconductors", "metrics": {"revenue_cagr": 50.0, "pat_cagr": 45.0, "roe": 24.0, "roce": 30.0, "operating_margin": 8.0, "debt_to_equity": 0.3, "interest_coverage": 12.0, "current_ratio": 1.5, "rd_percent": 2.0, "product_pipeline_score": 25, "market_cap_crs": 42000}},
    {"name": "KPIT Technologies", "symbol": "KPITTECH.NS", "sector": "Semiconductors", "metrics": {"revenue_cagr": 25.0, "pat_cagr": 30.0, "roe": 28.0, "roce": 32.0, "operating_margin": 19.0, "debt_to_equity": 0.1, "interest_coverage": 45.0, "current_ratio": 2.2, "rd_percent": 6.0, "product_pipeline_score": 40, "market_cap_crs": 45000}},

    # Clean Energy (20%)
    {"name": "Adani Green Energy", "symbol": "ADANIGREEN.NS", "sector": "Clean Energy", "metrics": {"revenue_cagr": 40.0, "pat_cagr": 50.0, "roe": 14.0, "roce": 11.0, "operating_margin": 65.0, "debt_to_equity": 3.0, "interest_coverage": 2.5, "current_ratio": 0.8, "rd_percent": 0.5, "product_pipeline_score": 10, "market_cap_crs": 310000}},
    {"name": "Tata Power", "symbol": "TATAPOWER.NS", "sector": "Clean Energy", "metrics": {"revenue_cagr": 18.0, "pat_cagr": 25.0, "roe": 15.0, "roce": 14.0, "operating_margin": 25.0, "debt_to_equity": 1.5, "interest_coverage": 3.5, "current_ratio": 0.9, "rd_percent": 1.0, "product_pipeline_score": 25, "market_cap_crs": 120000}},
    {"name": "Waaree Renewable", "symbol": "WAAREERTL.NS", "sector": "Clean Energy", "metrics": {"revenue_cagr": 30.0, "pat_cagr": 35.0, "roe": 25.0, "roce": 28.0, "operating_margin": 15.0, "debt_to_equity": 0.5, "interest_coverage": 8.0, "current_ratio": 1.5, "rd_percent": 2.0, "product_pipeline_score": 25, "market_cap_crs": 15000}},
    {"name": "IREDA", "symbol": "IREDA.NS", "sector": "Clean Energy", "metrics": {"revenue_cagr": 28.0, "pat_cagr": 38.0, "roe": 16.0, "roce": 18.0, "operating_margin": 85.0, "debt_to_equity": 5.0, "interest_coverage": 1.8, "current_ratio": 1.2, "rd_percent": 0.0, "product_pipeline_score": 0, "market_cap_crs": 45000}},
    {"name": "KPI Green Energy", "symbol": "KPIGREEN.NS", "sector": "Clean Energy", "metrics": {"revenue_cagr": 65.0, "pat_cagr": 80.0, "roe": 20.0, "roce": 22.0, "operating_margin": 35.0, "debt_to_equity": 2.0, "interest_coverage": 4.0, "current_ratio": 1.1, "rd_percent": 1.0, "product_pipeline_score": 10, "market_cap_crs": 12000}},

    # EV & Battery (15%)
    {"name": "Tata Motors", "symbol": "TATAMOTORS.NS", "sector": "EV & Battery", "metrics": {"revenue_cagr": 18.0, "pat_cagr": 15.0, "roe": 18.0, "roce": 15.0, "operating_margin": 15.0, "debt_to_equity": 1.2, "interest_coverage": 4.5, "current_ratio": 1.1, "rd_percent": 4.0, "product_pipeline_score": 40, "market_cap_crs": 350000}},
    {"name": "Exide Industries", "symbol": "EXIDEIND.NS", "sector": "EV & Battery", "metrics": {"revenue_cagr": 15.0, "pat_cagr": 12.0, "roe": 11.0, "roce": 14.0, "operating_margin": 12.0, "debt_to_equity": 0.1, "interest_coverage": 45.0, "current_ratio": 1.8, "rd_percent": 2.0, "product_pipeline_score": 25, "market_cap_crs": 28000}},
    {"name": "Amara Raja", "symbol": "ARE&M.NS", "sector": "EV & Battery", "metrics": {"revenue_cagr": 14.0, "pat_cagr": 11.0, "roe": 18.0, "roce": 20.0, "operating_margin": 14.0, "debt_to_equity": 0.05, "interest_coverage": 65.0, "current_ratio": 2.1, "rd_percent": 3.0, "product_pipeline_score": 25, "market_cap_crs": 15000}},
    {"name": "Olectra Greentech", "symbol": "OLECTRA.NS", "sector": "EV & Battery", "metrics": {"revenue_cagr": 55.0, "pat_cagr": 60.0, "roe": 12.0, "roce": 15.0, "operating_margin": 14.0, "debt_to_equity": 0.3, "interest_coverage": 8.0, "current_ratio": 1.5, "rd_percent": 4.0, "product_pipeline_score": 25, "market_cap_crs": 18000}},

    # Biotech (12%)
    {"name": "Dr Reddy's", "symbol": "DRREDDY.NS", "sector": "Biotech", "metrics": {"revenue_cagr": 12.0, "pat_cagr": 15.0, "roe": 17.0, "roce": 20.0, "operating_margin": 24.0, "debt_to_equity": 0.1, "interest_coverage": 55.0, "current_ratio": 2.5, "rd_percent": 8.0, "product_pipeline_score": 40, "market_cap_crs": 105000}},
    {"name": "Biocon", "symbol": "BIOCON.NS", "sector": "Biotech", "metrics": {"revenue_cagr": 18.0, "pat_cagr": 15.0, "roe": 8.0, "roce": 12.0, "operating_margin": 22.0, "debt_to_equity": 0.8, "interest_coverage": 6.0, "current_ratio": 1.4, "rd_percent": 12.0, "product_pipeline_score": 40, "market_cap_crs": 35000}},
    {"name": "Divi's Laboratories", "symbol": "DIVISLAB.NS", "sector": "Biotech", "metrics": {"revenue_cagr": 15.0, "pat_cagr": 18.0, "roe": 20.0, "roce": 25.0, "operating_margin": 30.0, "debt_to_equity": 0.0, "interest_coverage": 100.0, "current_ratio": 3.8, "rd_percent": 5.0, "product_pipeline_score": 25, "market_cap_crs": 110000}},

    # Defense (8%)
    {"name": "Bharat Electronics", "symbol": "BEL.NS", "sector": "Defense", "metrics": {"revenue_cagr": 15.0, "pat_cagr": 18.0, "roe": 25.0, "roce": 30.0, "operating_margin": 22.0, "debt_to_equity": 0.0, "interest_coverage": 100.0, "current_ratio": 1.9, "rd_percent": 8.0, "product_pipeline_score": 25, "market_cap_crs": 145000}},
    {"name": "HAL", "symbol": "HAL.NS", "sector": "Defense", "metrics": {"revenue_cagr": 12.0, "pat_cagr": 18.0, "roe": 28.0, "roce": 35.0, "operating_margin": 26.0, "debt_to_equity": 0.0, "interest_coverage": 100.0, "current_ratio": 2.2, "rd_percent": 8.0, "product_pipeline_score": 40, "market_cap_crs": 220000}},
    {"name": "Data Patterns", "symbol": "DATAPATTNS.NS", "sector": "Defense", "metrics": {"revenue_cagr": 35.0, "pat_cagr": 42.0, "roe": 20.0, "roce": 25.0, "operating_margin": 32.0, "debt_to_equity": 0.1, "interest_coverage": 25.0, "current_ratio": 2.8, "rd_percent": 10.0, "product_pipeline_score": 25, "market_cap_crs": 15000}}
]

for c_data in india_companies:
    # Add Company
    comp = Company(name=c_data["name"], symbol=c_data["symbol"], sector=c_data["sector"])
    db.add(comp)
    db.commit()
    db.refresh(comp)
    
    # Add Metrics
    m = c_data["metrics"]
    metrics = CompanyMetrics(
        company_id=comp.id,
        revenue_cagr=m["revenue_cagr"],
        pat_cagr=m["pat_cagr"],
        roe=m["roe"],
        roce=m["roce"],
        operating_margin=m["operating_margin"],
        debt_to_equity=m["debt_to_equity"],
        interest_coverage=m["interest_coverage"],
        current_ratio=m["current_ratio"],
        rd_percent=m["rd_percent"],
        product_pipeline_score=m["product_pipeline_score"],
        market_cap_crs=m["market_cap_crs"]
    )
    db.add(metrics)

db.commit()
db.close()
print("Future India Index seed data (Companies & Metrics) added successfully!")
