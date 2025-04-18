from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.schemas.sentiment import (
    SocialMediaPost, SocialMediaPostCreate,
    NewsArticle, NewsArticleCreate,
    EarningsCall, EarningsCallCreate,
    SentimentAnalysisResponse,
    TopicAnalysisResponse
)
from app.models.sentiment import SocialMediaPost as SocialMediaPostModel
from app.models.sentiment import NewsArticle as NewsArticleModel
from app.models.sentiment import EarningsCall as EarningsCallModel
from app.services.sentiment_service import SentimentService

router = APIRouter()
sentiment_service = SentimentService()

@router.post("/analyze/text", response_model=SentimentAnalysisResponse)
async def analyze_text(text: str):
    """Analyze sentiment of a single text"""
    result = sentiment_service.analyze_text(text)
    return {
        "sentiment_score": result["combined_score"],
        "sentiment_type": sentiment_service.get_sentiment_label(result["combined_score"]),
        "confidence": 1 - abs(result["vader_score"] - result["textblob_score"]) / 2,
        "details": result
    }

@router.post("/analyze/batch", response_model=SentimentAnalysisResponse)
async def analyze_texts(texts: List[str]):
    """Analyze sentiment of multiple texts"""
    result = sentiment_service.analyze_texts(texts)
    return result

@router.post("/analyze/earnings", response_model=SentimentAnalysisResponse)
async def analyze_earnings_call(transcript: str):
    """Analyze sentiment of an earnings call transcript"""
    result = sentiment_service.analyze_earnings_call(transcript)
    return result["overall_sentiment"]

@router.get("/social-media", response_model=List[SocialMediaPost])
async def get_social_media_posts(
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get social media posts with sentiment analysis"""
    query = db.query(SocialMediaPostModel)
    if source:
        query = query.filter(SocialMediaPostModel.source == source)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(SocialMediaPostModel.created_at >= cutoff_date)
    
    return query.order_by(SocialMediaPostModel.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/news", response_model=List[NewsArticle])
async def get_news_articles(
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get news articles with sentiment analysis"""
    query = db.query(NewsArticleModel)
    if source:
        query = query.filter(NewsArticleModel.source == source)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(NewsArticleModel.published_at >= cutoff_date)
    
    return query.order_by(NewsArticleModel.published_at.desc()).offset(skip).limit(limit).all()

@router.get("/earnings", response_model=List[EarningsCall])
async def get_earnings_calls(
    skip: int = 0,
    limit: int = 100,
    company: Optional[str] = None,
    ticker: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get earnings calls with sentiment analysis"""
    query = db.query(EarningsCallModel)
    if company:
        query = query.filter(EarningsCallModel.company == company)
    if ticker:
        query = query.filter(EarningsCallModel.ticker == ticker)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(EarningsCallModel.call_date >= cutoff_date)
    
    return query.order_by(EarningsCallModel.call_date.desc()).offset(skip).limit(limit).all()

@router.post("/earnings", response_model=EarningsCall)
async def create_earnings_call(
    earnings_call: EarningsCallCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new earnings call analysis"""
    # Analyze sentiment in the background
    sentiment_result = sentiment_service.analyze_earnings_call(earnings_call.transcript)
    
    db_earnings_call = EarningsCallModel(
        **earnings_call.model_dump(),
        overall_sentiment_score=sentiment_result["overall_sentiment"]["score"],
        overall_sentiment_type=sentiment_result["overall_sentiment"]["label"],
        confidence=sentiment_result["overall_sentiment"]["confidence"],
        topic_sentiments=sentiment_result["topic_sentiments"]
    )
    
    db.add(db_earnings_call)
    db.commit()
    db.refresh(db_earnings_call)
    
    return db_earnings_call 