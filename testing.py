from dhanhq import DhanContext, dhanhq

import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()  # This actually loads variables from .env into os.environ


dhan_context = DhanContext(os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN"))
print('client ID below:')
print(dhan_context.get_client_id)

dhan = dhanhq(dhan_context)

import datetime

from_date_str = '2025-03-10'
to_date_str='2025-03-10'
# from_date = datetime.datetime.strptime(from_date_str, '%Y-%m-%d').date()
# to_date = datetime.datetime.strptime(to_date_str, '%Y-%m-%d').date()

# daily_data = history.historical_daily_data(security_id='1333', exchange_segment=dhanhq.NSE, 
#                                      instrument_type='INDEX', expiry_code=0, from_date=from_date_str, to_date=to_date_str)
intra_day_data = dhan.intraday_minute_data(security_id='13', exchange_segment=dhanhq.INDEX, 
                                     instrument_type='INDEX', interval=5, from_date=from_date_str, to_date=to_date_str)
intra_day_df = pd.DataFrame(intra_day_data['data'])
intra_day_df.to_csv('intra_day_data_nifty_test.csv', index=False)


