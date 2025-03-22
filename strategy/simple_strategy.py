from strategy.input_format import Format_Input

class simple_strategy:
    def __init__(self):
        pass
    
    def run_strategy(self):
        print("Strategy Ran Successfully")
        arg_values = {}
        return arg_values
    
    def format_input(self):
        pass
    
    def execute_simple_strategy(self):
        arg_values = self.run_strategy()
        input_format = Format_Input(arg_values)
        orders = input_format.return_params()
        return orders

    
