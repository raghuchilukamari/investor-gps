from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..db.session import get_db
from ..crud import bls

router = APIRouter()

@router.get("/bls/indicators", response_model=List[Dict[str, Any]])
def get_bls_indicators(
    db: Session = Depends(get_db)
):
    """
    Get BLS indicators with their latest values and changes.
    """
    try:
        indicators = bls.get_indicators_matrix(db)
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

