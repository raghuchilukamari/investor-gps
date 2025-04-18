from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class SignalType(str, enum.Enum):
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"

class MacroIndicator(Base):
    __tablename__ = "macro_indicators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    value = Column(Float)
    previous_value = Column(Float)
    change = Column(Float)
    signal = Column(Enum(SignalType))
    source = Column(String)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    description = Column(String)
    category = Column(String)  # e.g., "inflation", "employment", "gdp", etc.
    frequency = Column(String)  # e.g., "daily", "weekly", "monthly", "quarterly"
    next_release = Column(DateTime(timezone=True), nullable=True) 