import pandas as pd
import numpy as np
from random import randint
from datetime import datetime
from morty.signals import EnterMarket
from morty.signals import ExitMarket

class Strategy:
    def __init__(self):
        # Program variables
        self.ticker = pd.DataFrame(index=[], columns=['mid_price'])
        self.pos_size = 1
        self.delta_enter = 0.05
        self.delta_exit = 0.20
        self.delta_stop_loss = 0.05
        self.max_short = 5

        # Strategy variables
        self.delta_time = 3600  # seconds

    def on_tick(self, tick, open_trades, balance):

        self.balance = balance

        # On tick, add it to pandas dataframe
        last = tick

        self.ticker.loc[datetime.utcfromtimestamp(last.timestamp)] = last.mid_price

        # Query the dataframe with last tick, and the closest ticker to the
        # starting time
        limit = int(last.timestamp) - int(self.delta_time)

        start = datetime.utcfromtimestamp(limit)
        end = datetime.utcfromtimestamp(int(last.timestamp))

        price_delta = self.get_price_delta(start, end)

        if (self.balance.asset1 > tick.avg_buy * self.pos_size and
                price_delta < self.delta_enter * -1):
            return EnterMarket('long', tick, self.pos_size)

        # if (self.balance.asset2_debt < self.max_short and
                # price_delta > self.delta_enter):
            # return EnterMarket('short', tick, self.pos_size)

        for trade in open_trades:
            if(trade.signal == 'long'):
                return self.long_trades(tick, trade)
            else:
                return self.short_trades(tick, trade)

        return False

    def get_price_delta(self, start, end):
        df = self.ticker.ix[start:end]
        first = df.iloc[0]['mid_price']
        last = df.iloc[-1]['mid_price']
        return ((last - first) / first)

    def short_trades(self, tick, trade):
        delta = ((tick.mid_price - trade.open_tick.mid_price) \
                / trade.open_tick.mid_price)

        if (delta > self.delta_stop_loss or delta < self.delta_exit * -1):
            return ExitMarket(tick, trade)

    def long_trades(self, tick, trade):
        delta = ((tick.mid_price - trade.open_tick.mid_price) \
                / trade.open_tick.mid_price)

        if (delta < self.delta_stop_loss * -1 or delta > self.delta_exit):
            return ExitMarket(tick, trade)

