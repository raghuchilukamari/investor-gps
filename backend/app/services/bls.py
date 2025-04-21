from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
import json
import logging
import prettytable
import sqlite3
import pandas as pd
from pandas import DataFrame

logger = logging.getLogger(__name__)

BLS_API_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"

# Common BLS series IDs for important economic indicators
SERIES_MAP = {
    "Consumer Price Index": "CUSR0000SA0",  # CPI - All Urban Consumers
    "Core CPI": "CUSR0000SA0L1E",  # CPI Less Food and Energy
    # "Producer Price Index": "WPUFD4",  # PPI for Final Demand
    "Producer Price Index": "WPSFD4",  # PPI for Final Demand
    "Unemployment Rate": "LNS14000000",  # Unemployment Rate
    "Nonfarm Payrolls": "CES0000000001",  # Total Nonfarm Employment
    "Average Hourly Earnings": "CES0500000003",  # Average Hourly Earnings
    "Labor Force Participation": "LNS11300000",  # Labor Force Participation Rate
    "Job Openings": "JTS000000000000000JOL",  # Job Openings Total Nonfarm
    # "Employment cost Index": "CIS1010000000000Q", # Quarterly
    "U.S. Import Price Index": "EIUIR", # Monthly for BEA End Use, All commodities, not seasonally adjusted
    "U.S. Export Price Index": "EIUIQ" # Monthly for BEA End Use, All commodities, not seasonally adjusted
}

class BLSError(Exception):
    pass

def fetch_bls_data(series_ids: List[str], start_year: str, end_year: str) -> Dict[str, Any]:
    """
    Fetch data from BLS API for given series IDs and date range
    """
    headers = {'Content-type': 'application/json'}
    data = json.dumps({
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year
    })
    
    try:
        response = requests.post(BLS_API_URL, data=data, headers=headers)
        response.raise_for_status()
        json_data = json.loads(response.text)
        
        if not json_data.get('Results'):
            raise BLSError("No results returned from BLS API")
            
        return json_data
    except requests.exceptions.RequestException as e:
        raise BLSError(f"Failed to fetch BLS data: {str(e)}")

def process_bls_data(data: List[Dict[str, Any]], series_id) -> tuple[DataFrame, DataFrame]:
    """
    Process BLS data and print it in a formatted table
    """
    series_name = next((k for k, v in SERIES_MAP.items() if v == series_id), 'Unknown')

    # Create DataFrame
    df = pd.DataFrame(data)
    df['value'] = pd.to_numeric(df['value'])
    df['series'] = series_name

    # Pivot the DataFrame
    pivoted_df = df.pivot(
        index=['series', 'year'],
        columns='period',
        values='value'
    ).reset_index()

    pivoted_df.columns.name = None

    # Calculate yoy change
    latest_mo = df[df['latest'] == 'true']['period'].values[0]
    latest_yr = df[df['latest'] == 'true']['year'].values[0]
    #pivoted_df['yoy_change'] = pivoted_df.groupby('series')[latest_mo].pct_change().round(3) * 100

    # Calculate mom change
    df_sorted = df.sort_values(by=['year','period'])
    df_sorted['mom_change'] = df_sorted.groupby('series')['value'].pct_change().round(3) * 100

    pivoted_df_sorted = df_sorted.pivot(
        index=['series', 'year'],
        columns='period',
        values='mom_change'
    ).reset_index()
    pivoted_df_sorted['yoy_change'] = pivoted_df.groupby('series')[latest_mo].pct_change().round(3) * 100
    pivoted_df_sorted.columns.name = None

    latest_mom_chg = pivoted_df_sorted[(pivoted_df_sorted['year'] == latest_yr)][latest_mo].values[0]
    latest_yoy_chg = pivoted_df_sorted[(pivoted_df_sorted['year'] == latest_yr)]['yoy_change'].values[0]

    summary_df = pd.DataFrame({
        'series name': series_name,
        'latest_mom_chg': latest_mom_chg,
        'latest_yoy_chg': latest_yoy_chg
    },index=[0])

    print(summary_df)
    print(f"Latest MOM change and YOY change for {series_name}: {latest_mom_chg}%, {latest_yoy_chg}%")

    return pivoted_df_sorted, summary_df

def store_bls_data_in_sqlite(mom_df, smry_df, series_id, db_path: str = "bls_data.db", is_first_call: bool = False) -> None:
    """
    Store BLS data in SQLite with the following schema:
    - Series as column index
    - Year as row index
    - Months/PeriodName as header row
    - Values in cells
    """
    try:
        # Create a connection to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop the table if it exists and this is the first call
        combined_table_name = "bls_combined_data"
        summary_table_name = "bls_summary_data"
        if is_first_call:
            cursor.execute(f"DROP TABLE IF EXISTS {combined_table_name}")
            logger.info(f"Dropped existing table {combined_table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {summary_table_name}")
            logger.info(f"Dropped existing table {summary_table_name}")

        # Store in SQLite
        mom_df.to_sql(combined_table_name, conn, if_exists='append', index=False)
        logger.info(f"Stored MOM data for {series_id} in table {combined_table_name}")

        smry_df.to_sql(summary_table_name, conn, if_exists='append', index=False)
        logger.info(f"Stored summary data for {series_id} in table {summary_table_name}")
        
        conn.close()
        logger.info("Successfully stored all BLS data in SQLite")
        
    except Exception as e:
        logger.error(f"Error storing BLS data in SQLite: {str(e)}")
        raise

def generate_sentiment(yoy_change: float) -> str:
    """
    Generate sentiment based on YoY and MoM changes
    """
    if yoy_change is None:
        return "Insufficient data"

    if yoy_change > 5:
        return "Strong inflationary pressure"
    elif yoy_change > 2:
        return "Moderate inflation"
    elif yoy_change > 0:
        return "Low inflation"
    elif yoy_change > -1:
        return "Deflationary pressure"
    else:
        return "Strong deflationary pressure"


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    current_year = str(datetime.now().year)
    last_year = str(int(current_year) - 1)
    
    try:
        # Fetch latest data from BLS
        bls_data = fetch_bls_data(
            series_ids=list(SERIES_MAP.values()),
            start_year=last_year,
            end_year=current_year
        )
        # Process and store data in SQLite
        is_first_call = True
        for series in bls_data['Results']['series']:
            data = series['data']
            series_id = series['seriesID']
            print(f"Processing data for {series['seriesID']}")
            mom_df,smry_df = process_bls_data(data, series_id)
            store_bls_data_in_sqlite(mom_df, smry_df, series_id, is_first_call=is_first_call)
            is_first_call = False

    except BLSError as e:
        logger.error(f"BLS API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}") 