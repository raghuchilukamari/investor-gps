from fredapi import Fred
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
import pandas as pd

load_dotenv()

class FREDService:
    def __init__(self):
        self.fred = Fred(api_key=os.getenv("FRED_API_KEY"))
        
    def get_series(self, series_id: str, days_back: int = 365) -> pd.DataFrame:
        """Fetch a time series from FRED"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        return self.fred.get_series(series_id, start_date, end_date)
    
    def get_latest_value(self, series_id: str) -> float:
        """Get the most recent value for a series"""
        series = self.get_series(series_id, days_back=1)
        return series.iloc[-1]
    
    def get_previous_value(self, series_id: str) -> float:
        """Get the previous value for a series"""
        series = self.get_series(series_id, days_back=2)
        return series.iloc[-2]
    
    def calculate_change(self, current: float, previous: float) -> float:
        """Calculate percentage change between two values"""
        return ((current - previous) / previous) * 100 if previous != 0 else 0
    
    def determine_signal(self, change: float, threshold: float = 0.5) -> str:
        """Determine signal based on percentage change"""
        if change > threshold:
            return "bullish"
        elif change < -threshold:
            return "bearish"
        return "neutral"
    
    def get_indicator_data(self, series_id: str, name: str, category: str) -> Dict:
        """Get complete indicator data including current value, previous value, and signal"""
        try:
            current = self.get_latest_value(series_id)
            previous = self.get_previous_value(series_id)
            change = self.calculate_change(current, previous)
            signal = self.determine_signal(change)
            
            return {
                "name": name,
                "value": current,
                "previous_value": previous,
                "change": change,
                "signal": signal,
                "source": "FRED",
                "description": f"FRED Series: {series_id}",
                "category": category,
                "frequency": "monthly"  # Default to monthly, can be overridden
            }
        except Exception as e:
            print(f"Error fetching data for {series_id}: {str(e)}")
            return None

# Common FRED series IDs
FRED_SERIES = {
    "GDP": "GDP",  # Gross Domestic Product
    "UNRATE": "UNRATE",  # Unemployment Rate
    "CPIAUCSL": "CPIAUCSL",  # Consumer Price Index
    "FEDFUNDS": "FEDFUNDS",  # Federal Funds Rate
    "M2": "M2",  # M2 Money Stock
    "INDPRO": "INDPRO",  # Industrial Production Index
    "RETAILSMNSA": "RETAILSMNSA",  # Retail Sales
    "HOUST": "HOUST",  # Housing Starts
    "PAYEMS": "PAYEMS",  # All Employees: Total Nonfarm
    "DGORDER": "DGORDER"  # Manufacturers' New Orders: Durable Goods
} 