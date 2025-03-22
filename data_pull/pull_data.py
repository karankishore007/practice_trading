from dhanhq import DhanContext, dhanhq

import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()  # This actually loads variables from .env into os.environ


dhan_context = DhanContext(os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN"))
dhan = dhanhq(dhan_context)

from_date_str = '2025-03-10'
to_date_str='2025-03-15'

# # Nifty Index Data Daily
# daily_data_nifty = dhan.historical_daily_data(security_id='13', exchange_segment=dhanhq.INDEX, 
#                                      instrument_type='INDEX', expiry_code=0, from_date=from_date_str, to_date=to_date_str)
# daily_data_nifty = pd.DataFrame(daily_data_nifty['data'])
# daily_data_nifty.to_csv('Data/daily_data_nifty.csv', index=False)

#Nifty Option Data daily
daily_data_nifty_fno = dhan.historical_daily_data(security_id='43868', exchange_segment=dhanhq.NSE_FNO, 
                                     instrument_type='OPTIDX', expiry_code=0, from_date=from_date_str, to_date=to_date_str)
print(daily_data_nifty_fno)
daily_data_nifty_fno = pd.DataFrame(daily_data_nifty_fno['data'])
daily_data_nifty_fno.to_csv('Data/daily_data_nifty_fno.csv', index=False)



# daily_data.to_csv('Data/daily_data.csv', index=False)

# intra_day_data_nifty_fno = dhan.intraday_minute_data(security_id='13', exchange_segment=dhanhq.NSE_FNO, 
#                                      instrument_type='IDX_I', interval=5, from_date=from_date_str, to_date=to_date_str)
# intra_day_data_nifty_fno = pd.DataFrame(intra_day_data_nifty_fno['data'])
# print(intra_day_data_nifty_fno)
# intra_day_data_nifty_fno.to_csv('Data/intra_day_data_nifty_fno.csv', index=False)
