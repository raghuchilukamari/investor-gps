from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class SentimentSource(str, enum.Enum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    NEWS = "news"
    EARNINGS = "earnings"

class SentimentType(str, enum.Enum):
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)  # twitter, reddit, etc.
    post_id = Column(String, unique=True, index=True)
    content = Column(Text)
    author = Column(String)
    created_at = Column(DateTime(timezone=True))
    sentiment_score = Column(Float)
    sentiment_type = Column(String)
    confidence = Column(Float)
    metadata = Column(JSON)
    created_at_db = Column(DateTime(timezone=True), server_default=func.now())

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    title = Column(String)
    content = Column(Text)
    url = Column(String, unique=True)
    published_at = Column(DateTime(timezone=True))
    sentiment_score = Column(Float)
    sentiment_type = Column(String)
    confidence = Column(Float)
    metadata = Column(JSON)
    created_at_db = Column(DateTime(timezone=True), server_default=func.now())

class EarningsCall(Base):
    __tablename__ = "earnings_calls"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    ticker = Column(String, index=True)
    call_date = Column(DateTime(timezone=True))
    transcript = Column(Text)
    overall_sentiment_score = Column(Float)
    overall_sentiment_type = Column(String)
    confidence = Column(Float)
    topic_sentiments = Column(JSON)  # Store topic-wise sentiments
    metadata = Column(JSON)
    created_at_db = Column(DateTime(timezone=True), server_default=func.now())

class MarketEvent(Base):
    __tablename__ = "market_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    description = Column(String)
    event_date = Column(DateTime(timezone=True))
    asset_reactions = Column(JSON)  # Store reactions for different asset classes
    aggregate_reaction = Column(JSON)
    created_at_db = Column(DateTime(timezone=True), server_default=func.now()) 