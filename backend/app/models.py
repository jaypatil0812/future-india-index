from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

# ✅ Import the single shared Base, engine, SessionLocal from database.py
from app.database import Base, engine, SessionLocal

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    symbol = Column(String, unique=True)
    sector = Column(String, index=True)
    
    metrics = relationship("CompanyMetrics", back_populates="company", uselist=False)

class CompanyMetrics(Base):
    __tablename__ = "company_metrics"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # Growth Score
    revenue_cagr = Column(Float)
    pat_cagr = Column(Float)
    
    # Profitability Score
    roe = Column(Float)
    roce = Column(Float)
    operating_margin = Column(Float)
    
    # Quality Score
    debt_to_equity = Column(Float)
    interest_coverage = Column(Float)
    current_ratio = Column(Float)
    
    # Innovation Score
    rd_percent = Column(Float)
    product_pipeline_score = Column(Integer)
    
    # Scale Score
    market_cap_crs = Column(Float)
    
    company = relationship("Company", back_populates="metrics")

class StockPrice(Base):
    __tablename__ = "stock_prices"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    date = Column(Date)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)

class CachedIndex(Base):
    __tablename__ = "cached_index"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    index_value = Column(Float)
    nifty_value = Column(Float)
