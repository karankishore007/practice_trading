from dhanhq import dhanhq, DhanContext
import os

dhan_context = DhanContext(os.getenv("CLIENT_ID"), os.getenv("ACCESS_TOKEN"))
dhan = dhanhq(dhan_context)

class Format_Input:
    def __init__(self, arg_values:list):
        self.arg_values = arg_values
        self.standard_input = {
                                "security_id": "1333",           # HDFC Bank
                                "exchange_segment": dhan.NSE,
                                "transaction_type": dhan.BUY,
                                "quantity": 1,
                                "order_type": dhan.MARKET,
                                "product_type": dhan.INTRA,
                                "price": 0,
                                "trigger_price":0, 
                                "disclosed_quantity":0,
                                "after_market_order":False, 
                                "validity":'DAY', 
                                "amo_time":'OPEN',
                                "bo_profit_value":None, 
                                "bo_stop_loss_Value":None, 
                                "tag":None, 
                                "should_slice":False
                                }
        # for arg in arg_values:
        #     print(arg)
        # if(arg_values["transaction_type"]=="SELL"):
        #     self.standard_input['transaction_type'] = dhan.SELL
    def return_params(self):
        params = self.standard_input
        print("Parammeters created as a list of acceptable arguments for order placing...")
        return [params]