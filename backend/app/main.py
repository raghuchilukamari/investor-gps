from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(
    title="Investor GPS API",
    description="Financial analytics platform API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Investor GPS API",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        },
        status_code=200
    )

# Import and include routers
# from app.api import macrometer, sentiment, market_reaction, earnings
# app.include_router(macrometer.router, prefix="/api/v1/macrometer", tags=["macrometer"])
# app.include_router(sentiment.router, prefix="/api/v1/sentiment", tags=["sentiment"])
# app.include_router(market_reaction.router, prefix="/api/v1/market-reaction", tags=["market-reaction"])
# app.include_router(earnings.router, prefix="/api/v1/earnings", tags=["earnings"]) 