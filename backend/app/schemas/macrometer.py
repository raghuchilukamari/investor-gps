from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.macrometer import SignalType

class MacroIndicatorBase(BaseModel):
    name: str
    value: float
    previous_value: float
    change: float
    signal: SignalType
    source: str
    description: str
    category: str
    frequency: str
    next_release: Optional[datetime] = None

class MacroIndicatorCreate(MacroIndicatorBase):
    pass

class MacroIndicatorUpdate(BaseModel):
    value: Optional[float] = None
    previous_value: Optional[float] = None
    change: Optional[float] = None
    signal: Optional[SignalType] = None
    last_updated: Optional[datetime] = None
    next_release: Optional[datetime] = None

class MacroIndicator(MacroIndicatorBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True 