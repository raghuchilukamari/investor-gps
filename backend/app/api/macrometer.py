from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.macrometer import MacroIndicator, MacroIndicatorCreate, MacroIndicatorUpdate
from app.models.macrometer import MacroIndicator as MacroIndicatorModel
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[MacroIndicator])
def get_macro_indicators(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(MacroIndicatorModel)
    if category:
        query = query.filter(MacroIndicatorModel.category == category)
    return query.offset(skip).limit(limit).all()

@router.get("/{indicator_id}", response_model=MacroIndicator)
def get_macro_indicator(indicator_id: int, db: Session = Depends(get_db)):
    indicator = db.query(MacroIndicatorModel).filter(MacroIndicatorModel.id == indicator_id).first()
    if indicator is None:
        raise HTTPException(status_code=404, detail="Macro indicator not found")
    return indicator

@router.post("/", response_model=MacroIndicator)
def create_macro_indicator(
    indicator: MacroIndicatorCreate,
    db: Session = Depends(get_db)
):
    db_indicator = MacroIndicatorModel(**indicator.model_dump())
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

@router.put("/{indicator_id}", response_model=MacroIndicator)
def update_macro_indicator(
    indicator_id: int,
    indicator: MacroIndicatorUpdate,
    db: Session = Depends(get_db)
):
    db_indicator = db.query(MacroIndicatorModel).filter(MacroIndicatorModel.id == indicator_id).first()
    if db_indicator is None:
        raise HTTPException(status_code=404, detail="Macro indicator not found")
    
    update_data = indicator.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_indicator, field, value)
    
    db_indicator.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

@router.delete("/{indicator_id}")
def delete_macro_indicator(indicator_id: int, db: Session = Depends(get_db)):
    db_indicator = db.query(MacroIndicatorModel).filter(MacroIndicatorModel.id == indicator_id).first()
    if db_indicator is None:
        raise HTTPException(status_code=404, detail="Macro indicator not found")
    
    db.delete(db_indicator)
    db.commit()
    return {"message": "Macro indicator deleted successfully"} 