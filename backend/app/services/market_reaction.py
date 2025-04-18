import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class MarketReactionService:
    def __init__(self):
        self.asset_classes = {
            "stocks": "^GSPC",  # S&P 500
            "bonds": "^TNX",    # 10-year Treasury yield
            "gold": "GC=F",     # Gold futures
            "dollar": "DX-Y.NYB"  # Dollar index
        }
    
    def get_asset_data(self, symbol: str, days_back: int = 5) -> pd.DataFrame:
        """Fetch historical data for an asset"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        try:
            data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def calculate_reaction(self, data: pd.DataFrame, event_date: datetime) -> Dict:
        """Calculate market reaction around an event"""
        if data.empty:
            return {
                "pre_event": None,
                "event_day": None,
                "post_event": None,
                "total_change": None,
                "volatility": None
            }
        
        # Convert event_date to datetime if it's a string
        if isinstance(event_date, str):
            event_date = pd.to_datetime(event_date)
        
        # Get data around event
        pre_event = data[data.index < event_date].iloc[-1]["Close"] if not data[data.index < event_date].empty else None
        event_day = data[data.index == event_date]["Close"].iloc[0] if not data[data.index == event_date].empty else None
        post_event = data[data.index > event_date].iloc[0]["Close"] if not data[data.index > event_date].empty else None
        
        # Calculate changes
        total_change = ((post_event - pre_event) / pre_event * 100) if pre_event and post_event else None
        volatility = data["Close"].pct_change().std() * 100 if not data.empty else None
        
        return {
            "pre_event": pre_event,
            "event_day": event_day,
            "post_event": post_event,
            "total_change": total_change,
            "volatility": volatility
        }
    
    def analyze_market_reaction(self, event_date: datetime, event_type: str, event_description: str) -> Dict:
        """Analyze market reactions across all asset classes"""
        reactions = {}
        
        for asset_class, symbol in self.asset_classes.items():
            data = self.get_asset_data(symbol)
            reaction = self.calculate_reaction(data, event_date)
            reactions[asset_class] = reaction
        
        # Calculate aggregate reaction
        changes = [r["total_change"] for r in reactions.values() if r["total_change"] is not None]
        avg_change = np.mean(changes) if changes else None
        
        return {
            "event_type": event_type,
            "event_description": event_description,
            "event_date": event_date.isoformat(),
            "asset_reactions": reactions,
            "aggregate_reaction": {
                "average_change": avg_change,
                "direction": "bullish" if avg_change and avg_change > 0 else "bearish" if avg_change and avg_change < 0 else "neutral"
            }
        }
    
    def get_historical_reactions(self, event_type: str, days_back: int = 30) -> List[Dict]:
        """Get historical market reactions for a specific event type"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        reactions = []
        for asset_class, symbol in self.asset_classes.items():
            data = self.get_asset_data(symbol, days_back=days_back)
            if not data.empty:
                daily_changes = data["Close"].pct_change()
                significant_changes = daily_changes[abs(daily_changes) > daily_changes.std() * 2]
                
                for date, change in significant_changes.items():
                    reactions.append({
                        "date": date.isoformat(),
                        "asset_class": asset_class,
                        "change": change * 100,
                        "direction": "bullish" if change > 0 else "bearish"
                    })
        
        return sorted(reactions, key=lambda x: x["date"], reverse=True) 