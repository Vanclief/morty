import pandas as pd
from datetime import datetime

class Tick:
    def __init__(self, tick, ticker):
        self.tick = tick
        self.ticker = ticker
        self.timestamp = float(tick['Timestamp'])
        self.avg_buy = float(tick['Avg_Buy'])
        self.avg_sell = float(tick['Avg_Sell'])
        self.mid_price = (self.avg_buy + self.avg_sell) /2

    def print_tick(self):
        date = datetime.utcfromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        print('{:} B: {:} S: {:} M: {:}'.format(date, self.avg_buy,
            self.avg_sell, self.mid_price))
