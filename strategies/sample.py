import pandas as pd
import numpy as np
from morty.backtest import Backtester

class Sample:
    def __init__(self):
        self.mid_list = []
        self.asset1_balance = 1000
        self.asset2_balance = 0

    # TODO on tick should also return the complete balance, also maybe add a
    # "can trade" function

    def on_tick(self, tick, open_trades, asset1_balance):
        """
        This is the only required function the Strategy Class must have, it
        is called by the Backtester every single time there is a "tick" in the
        order book.

        Returns:
            tick, open_trades

        Tick attributes:
            Timestamp (Time in seconds since EPOCH)
            Avg_Buy (Avg buying price for the specified depth )
            Avg_Sell (Avg selling price for the specified depth )
            Asset1_balance (Balance of asset 1)

        open_trades attributes:
            signal (Trade signal: short or long)
            amount (Trade size)
            pair (Trading pair)
            time (Time the trade was placed in timestamp)
            avg_buy
            avg_sell
            mid_price

        -------------------
        Available functions:
        -------------------
        bt.trade(<Signal>, <Tick>, <Amount>)
        bt.close_trade(<Tick>, <Trade>)

        """

        # if (tick.timestamp > 1499759181):
            # bt.trade('short', tick, 0.1)

        sma10 = self.get_sma(tick, 10)

        if (len(self.mid_list) < 10):
            return

        if (self.asset1_balance > 300 and sma10 < tick.avg_sell):
            balance = bt.trade('long', tick, 0.2)
            self.asset1_balance = balance[0]


        for trade in open_trades:
            if(trade.signal == 'long'):
                self.long_trades(tick, trade, sma10)
            else:
                self.short_trades(tick, trade)

    def short_trades(self, tick, trade):
        bt.close_trade(tick, trade)

    def long_trades(self, tick, trade, sma10):

        if (sma10 > tick.avg_buy):
            bt.close_trade(tick, trade)

    def get_sma(self, tick, sma_size):
        mid_price = (tick.avg_sell + tick.avg_buy)/2
        self.mid_list.append(mid_price)
        return self.sma(self.mid_list, sma_size)

    def sma(self, x, N):
        return np.convolve(x, np.ones((N,))/N, mode='valid')[-1]

pair = 'ETH-EUR'
bt = Backtester(pair, 1000)

bt.add_strategy(Sample())
bt.add_data('Kraken', 5, 10)
bt.run()
bt.end()
# bt.plot()

