import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ssl
import urllib.request
from dhanhq import DhanContext, dhanhq
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime

load_dotenv()  # This actually loads variables from .env into os.environ

dhan_context = DhanContext(os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN"))
print('client ID below:')
print(dhan_context.get_client_id)

dhan = dhanhq(dhan_context)

# SSL workaround to avoid certificate verification issues
ssl._create_default_https_context = ssl._create_unverified_context

# Import F&O stock details from DHAN CSV
SCRIP_MASTER_URL = "https://images.dhan.co/api-data/api-scrip-master-detailed.csv"
scrip_master_filename = "dhan_scrip_master.csv"
urllib.request.urlretrieve(SCRIP_MASTER_URL, scrip_master_filename)

dhan_scrips = pd.read_csv(scrip_master_filename)

# Save the imported scrip master CSV
dhan_scrips.to_csv(scrip_master_filename, index=False)

# Manually curated list of all F&O stocks traded on NSE
FNO_STOCKS = [
    "ACC","ADANIENT"
]

# Save F&O stocks to CSV
df = pd.DataFrame(FNO_STOCKS, columns=["Stock Symbol"])
fno_stocks_filename = "fno_stocks_list.csv"
df.to_csv(fno_stocks_filename, index=False)

# Find F&O stocks data in Dhan scrips
dhan_fno_stocks = dhan_scrips[(dhan_scrips['UNDERLYING_SYMBOL'].isin(FNO_STOCKS)) & 
                              (dhan_scrips['EXCH_ID'] == 'NSE') & 
                              (dhan_scrips['SEGMENT'] == 'E') & 
                              (dhan_scrips['INSTRUMENT'] == 'EQUITY')]
print(dhan_fno_stocks)

# Store security IDs in a list
security_ids = dhan_fno_stocks['SECURITY_ID'].tolist()

# Define date range and other parameters
from_date = "2025-03-21"
to_date = "2025-03-22"
instrument_type = "EQUITY"
exchange_segment = dhanhq.NSE
interval=5
expiry_code = 0

# Initialize an empty DataFrame to store all historical data
all_historical_data = pd.DataFrame()

def fetch_historical_data(security_id, from_date, to_date):
    """Fetch intraday minute data using DHAN API and clean the response."""
    intra_day_data = dhan.intraday_minute_data(
        security_id=security_id,
        exchange_segment=exchange_segment,
        instrument_type=instrument_type,
        interval=interval,
        from_date=from_date,
        to_date=to_date
    )
    
    # Ensure response contains data
    if not intra_day_data or 'data' not in intra_day_data:
        print(f"No data found for security ID: {security_id}")
        return None

    # Convert JSON response to DataFrame
    df = pd.DataFrame(intra_day_data['data'])

    # Convert timestamp to a readable format and convert to IST
    df['timestamp'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(int(x), pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d-%m-%y %H:%M'))
    df['security_id'] = security_id  # Add security_id for reference
    
    # Reorder columns
    df = df[['security_id', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]
    
    return df

def analyze_smart_money(historical_data):
    """Analyze smart money activity based on price, volume, and VWAP."""
    historical_data['VWAP'] = (historical_data['volume'] * (historical_data['high'] + historical_data['low'] + historical_data['close']) / 3).cumsum() / historical_data['volume'].cumsum()
    
    historical_data['Price_Volume_Divergence'] = np.where(
        (historical_data['close'] > historical_data['VWAP']) & (historical_data['volume'] > historical_data['volume'].rolling(10).mean()), 'Bullish',
        np.where((historical_data['close'] < historical_data['VWAP']) & (historical_data['volume'] > historical_data['volume'].rolling(10).mean()), 'Bearish', 'Neutral')
    )
    
    return historical_data[['timestamp', 'security_id', 'close', 'VWAP', 'volume', 'Price_Volume_Divergence']]

def plot_smart_money_analysis(historical_data, security_id):
    """Plot price vs VWAP along with volume for smart money analysis."""
    plt.figure(figsize=(12, 6))
    plt.plot(historical_data['timestamp'], historical_data['close'], label='Close Price', color='blue')
    plt.plot(historical_data['timestamp'], historical_data['VWAP'], label='VWAP', color='orange', linestyle='dashed')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Smart Money Analysis for {security_id}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Show data values on the graph
    for i, txt in enumerate(historical_data['close']):
        plt.text(i, historical_data['close'].iloc[i], f'{txt:.2f}', fontsize=9, verticalalignment='bottom')
    
    plt.show()

if __name__ == "__main__":
    for security_id in security_ids:
        df = fetch_historical_data(security_id, from_date, to_date)
        if df is not None:
            all_historical_data = pd.concat([all_historical_data, df], ignore_index=True)
    
    # Save all historical data into a single CSV file
    all_historical_data.to_csv("all_historical_data.csv", index=False, header=True)

    # Analyze smart money activity
    if not all_historical_data.empty:
        analyzed_data = analyze_smart_money(all_historical_data)
        analyzed_data.to_csv("smart_money_analysis.csv", index=False, header=True)
        print("Smart Money Analysis saved to smart_money_analysis.csv")

        # Plot for each security
        unique_security_ids = all_historical_data['security_id'].unique()
        for sec_id in unique_security_ids:
            sec_data = analyzed_data[analyzed_data['security_id'] == sec_id]
            plot_smart_money_analysis(sec_data, sec_id)
