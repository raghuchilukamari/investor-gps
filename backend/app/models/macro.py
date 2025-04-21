from sqlalchemy import Column, Integer, String, Float, Date, Enum, DateTime, Text, Index, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
from sqlalchemy import Boolean

Base = declarative_base()

class MacroIndicator(Base):
    __tablename__ = "macro_indicators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    series_id = Column(String, index=True)  # BLS series ID
    value = Column(Float)
    change = Column(Float)  # Period-over-period change
    unit = Column(String)  # e.g., "Percent", "Index", "Value", "Thousands"
    period = Column(String)  # e.g., "January 2024"
    frequency = Column(String)  # e.g., "Monthly", "Quarterly"
    footnotes = Column(Text)  # BLS footnotes
    last_updated = Column(DateTime, default=datetime.utcnow)

class EconomicEvent(Base):
    __tablename__ = "economic_events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    signal = Column(String, nullable=True)
    macro_impact = Column(String, nullable=True)

class PolicyOutlook(Base):
    __tablename__ = "policy_outlook"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String, index=True)
    outlook = Column(String)
    description = Column(String, nullable=True)

class CrossAssetImpact(Base):
    __tablename__ = "cross_asset_impact"

    id = Column(Integer, primary_key=True, index=True)
    asset = Column(String, index=True)
    macro_impact = Column(String)
    description = Column(String, nullable=True)

class Indicator(Base):
    """Main table for storing indicator metadata"""
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "Consumer Price Index"
    series_id = Column(String, unique=True, index=True)  # BLS series ID
    description = Column(Text)
    frequency = Column(String)  # e.g., "Monthly"
    unit = Column(String)  # e.g., "Index", "Percent", "Thousands"
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationship to time series data points
    data_points = relationship("TimeSeriesPoint", back_populates="indicator")

class TimeSeriesPoint(Base):
    """Table for storing individual time series data points"""
    __tablename__ = "time_series_points"

    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)  # 1-12 for monthly data
    value = Column(Float)
    footnotes = Column(Text)
    is_preliminary = Column(Boolean, default=False)
    is_revised = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Create a composite index for efficient time series queries
    __table_args__ = (
        Index('idx_indicator_time', 'indicator_id', 'year', 'month'),
    )

    # Relationship back to the indicator
    indicator = relationship("Indicator", back_populates="data_points")

class IndicatorRevision(Base):
    """Table for tracking revisions to indicator values"""
    __tablename__ = "indicator_revisions"

    id = Column(Integer, primary_key=True)
    time_series_point_id = Column(Integer, ForeignKey("time_series_points.id"), index=True)
    previous_value = Column(Float)
    new_value = Column(Float)
    revision_date = Column(DateTime, default=datetime.utcnow)
    revision_note = Column(Text)

class IndicatorMetadata(Base):
    """Table for storing additional metadata about indicators"""
    __tablename__ = "indicator_metadata"

    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), unique=True)
    seasonal_adjustment = Column(String)  # e.g., "Seasonally Adjusted", "Not Seasonally Adjusted"
    base_period = Column(String)  # e.g., "1982-84=100" for CPI
    calculation_method = Column(Text)
    update_frequency = Column(String)  # e.g., "Monthly", "Annual"
    release_schedule = Column(Text)  # JSON field for release schedule information

class MacroSeries(Base):
    """Table for storing macro series metadata"""
    __tablename__ = "macro_series"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(String, unique=True, index=True)  # BLS series ID
    name = Column(String, index=True)  # Human-readable name
    frequency = Column(String)  # e.g., "Monthly", "Quarterly"
    last_updated = Column(DateTime, default=datetime.utcnow)
    next_update = Column(DateTime)  # Expected next update date
    description = Column(String, nullable=True)  # Optional description
    unit = Column(String)  # e.g., "Percent", "Index", "Thousands"
    seasonal_adjustment = Column(String, nullable=True)  # e.g., "Seasonally Adjusted", "Not Seasonally Adjusted"
    
    # Relationship to data points
    data_points = relationship("MacroData", back_populates="series")

class MacroData(Base):
    """Table for storing macro data in matrix format"""
    __tablename__ = "macro_data"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(String, ForeignKey("macro_series.series_id"))
    year = Column(Integer, index=True)
    month = Column(Integer)  # 1-12 for monthly data
    value = Column(Float)
    change = Column(Float)  # Year-over-year change
    footnotes = Column(String, nullable=True)
    is_preliminary = Column(Boolean, default=False)
    is_revised = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to series metadata
    series = relationship("MacroSeries", back_populates="data_points")

    class Config:
        orm_mode = True 