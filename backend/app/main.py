from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import Base, engine, SessionLocal
from app.routes import stocks, companies, index
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.services.index_cacher import update_index_cache

# Initialise Background Scheduler
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run once on startup to warm the cache
    scheduler.add_job(update_index_cache, 'interval', hours=1)
    scheduler.start()
    
    # Run an immediate manual fetch
    print("Warming background index cache...")
    try:
        update_index_cache()
    except Exception as e:
        print("Failed to warm cache:", e)
        
    yield
    
    # Clean shutdown
    scheduler.shutdown()


# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Market Dashboard", lifespan=lifespan)

# ✅ Enable CORS
origins = [
    "http://localhost:3000",   # frontend react
    "http://127.0.0.1:3000",
    "https://stock-market-dashboard-tan.vercel.app",
    "https://frontend-gamma-dun-15.vercel.app",
    "https://4c4e77aab54dee60-160-20-123-9.serveousercontent.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # frontend allowed
    allow_credentials=True,
    allow_methods=["*"],            # allow all methods (GET, POST etc.)
    allow_headers=["*"],            # allow all headers
)

# Attach routers
app.include_router(index.router, prefix="/index", tags=["index"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
app.include_router(companies.router, prefix="/companies", tags=["companies"])
