from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.schemas.sentiment import MarketEvent, MarketEventCreate
from app.models.sentiment import MarketEvent as MarketEventModel
from app.services.market_reaction import MarketReactionService

router = APIRouter()
market_service = MarketReactionService()

@router.post("/analyze", response_model=MarketEvent)
async def analyze_market_reaction(
    event_type: str,
    event_description: str,
    event_date: datetime,
    db: Session = Depends(get_db)
):
    """Analyze market reaction to a specific event"""
    result = market_service.analyze_market_reaction(event_date, event_type, event_description)
    
    # Store the analysis in the database
    db_event = MarketEventModel(
        event_type=event_type,
        description=event_description,
        event_date=event_date,
        asset_reactions=result["asset_reactions"],
        aggregate_reaction=result["aggregate_reaction"]
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.get("/events", response_model=List[MarketEvent])
async def get_market_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get historical market events and their reactions"""
    query = db.query(MarketEventModel)
    if event_type:
        query = query.filter(MarketEventModel.event_type == event_type)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(MarketEventModel.event_date >= cutoff_date)
    
    return query.order_by(MarketEventModel.event_date.desc()).offset(skip).limit(limit).all()

@router.get("/historical/{event_type}", response_model=List[dict])
async def get_historical_reactions(
    event_type: str,
    days_back: int = 30
):
    """Get historical market reactions for a specific event type"""
    return market_service.get_historical_reactions(event_type, days_back)

@router.get("/asset/{asset_class}", response_model=dict)
async def get_asset_data(
    asset_class: str,
    days_back: int = 5
):
    """Get historical data for a specific asset class"""
    if asset_class not in market_service.asset_classes:
        raise HTTPException(status_code=400, detail="Invalid asset class")
    
    symbol = market_service.asset_classes[asset_class]
    data = market_service.get_asset_data(symbol, days_back)
    
    if data.empty:
        raise HTTPException(status_code=404, detail="No data available for this asset class")
    
    return {
        "asset_class": asset_class,
        "symbol": symbol,
        "data": data.to_dict(orient="records")
    }

@router.get("/summary", response_model=dict)
async def get_market_summary():
    """Get a summary of current market conditions across all asset classes"""
    summary = {}
    
    for asset_class, symbol in market_service.asset_classes.items():
        data = market_service.get_asset_data(symbol, days_back=1)
        if not data.empty:
            current_price = data["Close"].iloc[-1]
            daily_change = data["Close"].pct_change().iloc[-1] * 100
            
            summary[asset_class] = {
                "current_price": current_price,
                "daily_change": daily_change,
                "direction": "bullish" if daily_change > 0 else "bearish" if daily_change < 0 else "neutral"
            }
    
    return summary 