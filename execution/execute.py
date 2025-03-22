from dhanhq import DhanContext, dhanhq
import os
from strategy.simple_strategy import simple_strategy

from dotenv import load_dotenv
load_dotenv()  # This actually loads variables from .env into os.environ


dhan_context = DhanContext(os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN"))
dhan = dhanhq(dhan_context)

strategy = simple_strategy()
orders = strategy.execute_simple_strategy()

for order_params in orders:
    print(order_params)
    response = dhan.place_order(**order_params)
    print(response)


