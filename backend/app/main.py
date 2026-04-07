from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

# ✅ Import the unified Base/engine from database.py
from app.database import Base, engine, SessionLocal
# ✅ Import models so all tables are registered on Base
from app import models
from app.models import Company
from app.routes import stocks, companies, index
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.services.index_cacher import update_index_cache

# Initialise Background Scheduler
scheduler = BackgroundScheduler()

# ✅ Create all tables (Company, CompanyMetrics, StockPrice, CachedIndex)
Base.metadata.create_all(bind=engine)

# ✅ Auto-seed if the database is empty
def auto_seed():
    db = SessionLocal()
    try:
        count = db.query(Company).count()
        if count == 0:
            print("Database is empty on Render. Running seed script...")
            from app.seed import seed_db
            seed_db()
            print("Seed complete!")
        else:
            print(f"Database already has {count} companies. Skipping seed.")
    except Exception as e:
        print(f"Auto-seed error: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Seed database if empty
    auto_seed()
    
    # 2. Start background scheduler for hourly data updates
    scheduler.add_job(update_index_cache, 'interval', hours=1)
    scheduler.start()
    
    import asyncio
    
    # 3. Warm the cache immediately at startup in a non-blocking thread
    print("Scheduling background index cache warm-up...")
    try:
        asyncio.create_task(asyncio.to_thread(update_index_cache))
    except Exception as e:
        print("Failed to schedule warm cache task:", e)
        
    yield
    
    # Clean shutdown
    scheduler.shutdown()


app = FastAPI(title="Stock Market Dashboard", lifespan=lifespan)

# ✅ Enable CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://stock-market-dashboard-tan.vercel.app",
    "https://frontend-gamma-dun-15.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach routers
app.include_router(index.router, prefix="/index", tags=["index"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
app.include_router(companies.router, prefix="/companies", tags=["companies"])
