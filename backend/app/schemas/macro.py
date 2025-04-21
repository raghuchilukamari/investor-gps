from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class MacroIndicatorResponse(BaseModel):
    name: str
    latest_value: float
    latevavor: float
    change: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class EconomicEventResponse(BaseModel):
    name: str
    date: date
    signal: Optional[str] = None
    macro_impact: Optional[str] = None

    class Config:
        orm_mode = True

class PolicyOutlookResponse(BaseModel):
    institution: str
    outlook: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class CrossAssetImpactResponse(BaseModel):
    asset: str
    macro_impact: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class DashboardResponse(BaseModel):
    indicators: List[MacroIndicatorResponse]
    events: List[EconomicEventResponse]
    policies: List[PolicyOutlookResponse]
    impacts: List[CrossAssetImpactResponse]

    class Config:
        orm_mode = True 