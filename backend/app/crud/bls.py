from pandas import DataFrame
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import pandas as pd

def get_indicators_matrix(db: Session) -> List[Dict[str, Any]]:
    """
    Get BLS indicators with their latest values and changes.
    """
    query = "SELECT * FROM bls_summary_data"
    df = pd.read_sql_query(query, db.bind)
    return df.to_dict('records')

def get_matrix_data(db: Session) -> List[Dict[str, Any]]:
    """
    Get matrix data from materialized view.
    """
    query = """
    SELECT * FROM bls_combined_data
    """
    
    df = pd.read_sql_query(query, db.bind)
    return df.to_dict('records')

def map_series_id_to_name(series_id: str) -> str:
    """
    Map BLS series ID to a human-readable name
    """
    series_map = {
        "CUUR0000SA0": "Consumer Price Index",
        "CUSR0000SA0L1E": "Core CPI",
        "WPSFD4": "Producer Price Index",
        "LNS14000000": "Unemployment Rate",
        "CES0000000001": "Nonfarm Payrolls",
        "CES0500000003": "Average Hourly Earnings",
        "LNS11300000": "Labor Force Participation",
        "JTS000000000000000JOL": "Job Openings",
        "ICSA": "Initial Jobless Claims",
        "IPS10": "Industrial Production",
        "EIUIR": "U.S. Import Price Index",
        "EIUIQ": "U.S. Export Price Index"
    }
    
    return series_map.get(series_id, series_id)
