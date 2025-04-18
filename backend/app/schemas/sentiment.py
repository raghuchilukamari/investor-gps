from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, List, Any
from app.models.sentiment import SentimentSource, SentimentType

class SocialMediaPostBase(BaseModel):
    source: str
    post_id: str
    content: str
    author: str
    created_at: datetime
    sentiment_score: float
    sentiment_type: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None

class SocialMediaPostCreate(SocialMediaPostBase):
    pass

class SocialMediaPost(SocialMediaPostBase):
    id: int
    created_at_db: datetime

    class Config:
        from_attributes = True

class NewsArticleBase(BaseModel):
    source: str
    title: str
    content: str
    url: str
    published_at: datetime
    sentiment_score: float
    sentiment_type: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticle(NewsArticleBase):
    id: int
    created_at_db: datetime

    class Config:
        from_attributes = True

class TopicSentiment(BaseModel):
    topic: str
    score: float
    sentiment: str

class EarningsCallBase(BaseModel):
    company: str
    ticker: str
    call_date: datetime
    transcript: str
    overall_sentiment_score: float
    overall_sentiment_type: str
    confidence: float
    topic_sentiments: Dict[str, float]
    metadata: Optional[Dict[str, Any]] = None

class EarningsCallCreate(EarningsCallBase):
    pass

class EarningsCall(EarningsCallBase):
    id: int
    created_at_db: datetime

    class Config:
        from_attributes = True

class AssetReaction(BaseModel):
    pre_event: Optional[float]
    event_day: Optional[float]
    post_event: Optional[float]
    total_change: Optional[float]
    volatility: Optional[float]

class AggregateReaction(BaseModel):
    average_change: Optional[float]
    direction: str

class MarketEventBase(BaseModel):
    event_type: str
    description: str
    event_date: datetime
    asset_reactions: Dict[str, AssetReaction]
    aggregate_reaction: AggregateReaction

class MarketEventCreate(MarketEventBase):
    pass

class MarketEvent(MarketEventBase):
    id: int
    created_at_db: datetime

    class Config:
        from_attributes = True

class SentimentAnalysisResponse(BaseModel):
    sentiment_score: float
    sentiment_type: str
    confidence: float
    details: Optional[Dict[str, Any]] = None

class TopicAnalysisResponse(BaseModel):
    topic: str
    sentiment_score: float
    sentiment_type: str
    mentions: int
    key_phrases: List[str] 