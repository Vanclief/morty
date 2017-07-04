""" Core Trading Engine """

import time
import sys
import pandas as pd
import importlib.util
from configparser import SafeConfigParser
from morty.tick import Tick
from morty.fees import Fees
from morty.trade import Trade
from morty.balance import Balance
from morty.tcolors import Tcolors
from morty.backfill import Backfiller
from morty.report import Reporter
from morty.signals import EnterMarket
from morty.signals import ExitMarket

tc = Tcolors()

class Engine:

    def __init__(self, pair, exchange, strategy):
        self.trades = []
        self.pair = pair
        self.exchange = exchange
        self.get_exchange_fees(exchange)
        self.add_strategy(strategy)

    def get_exchange_fees(self, exchange):
        parser = SafeConfigParser()
        parser.read('fees.ini')
        maker = (parser.get(exchange, 'maker'))
        taker = (parser.get(exchange, 'taker'))
        self.fees = Fees(maker, taker)

    def add_strategy(self, strategy):
        """
        Add a Strategy Object, which contains the required
        trading signals
        """
        spec = importlib.util.spec_from_file_location(strategy,
                "./strategies/" + strategy + ".py")
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        self.strategy = imported_module.Strategy()

    def backfill_data(self, depth, days):
        """
        Backfill the required dataset, should be a Pandas dataframe. Keep last
        price if there are multiple elements with the same timestamp.
        """
        self.days = int(days)
        bf = Backfiller(self.exchange, self.balance.pair, depth, days)
        self.data = bf.run()

    def get_live_data(self, depth):
        """
        Get live data
        """
        print("WIP")

    def set_balance(self, initial_balance):
        self.balance = Balance(self.pair, initial_balance)

    def get_tick(self, time):
        """
        Get a single tick, defined as a row of the dataset.
        """
        return Tick(self.data.loc[self.data['Timestamp'] == time], self.data)

    def buy(self, price, amount):
        """
        Perfom a buy, defined as exchanging asset1 for asset2
        Returns if pucharse was successful
        """
        if (self.balance.asset1 >= price * amount):
            self.balance.asset1 -= price * amount * (1 + self.fees.taker)
            self.balance.asset2 += amount
            return True
        else:
            print(tc.colorize_s(tc.red, "ERROR: Insuficient Asset1"))
            return False

    def sell(self, price, amount):
        """
        Perfom a buy, defined as exchanging asset2 for asset1
        Returns if pucharse was successful
        """
        if (self.balance.asset2 >= amount):
            self.balance.asset1 += price * amount * (1 - self.fees.taker)
            self.balance.asset2 -= amount
            return True
        else:
            print(tc.colorize_s(tc.red, "ERROR: Insuficient Asset2 "))
            return False

    def short(self, price, amount):
        """
        Perfom a short, defined as exchanging asset2 for asset1
        """
        self.balance.asset2_debt += amount
        return True

    def buy_back(self, tick, trade):
        """
        Closes a short position
        """
        self.balance.asset1 += (trade.open_tick.avg_buy - tick.avg_sell) \
                * trade.amount * (1 - self.fees.taker)
        self.balance.asset2_debt -= trade.amount
        return True

    def open_trade(self, signal, tick, amount):
        """
        This function handles the logic of performing a trade.
        """

        if (signal == 'long'):
            valid = self.buy(tick.avg_sell, amount)

        elif (signal == 'short'):
            valid = self.short(tick.avg_buy, amount)

        if (valid):
            trade = Trade(signal, amount, tick, self.balance)
            self.trades.append(trade)

        return self.balance

    def close_trade(self, tick, trade):
        """
        This function handles the logic of closing a trade
        """
        if (not trade.isopen):
            return
        if (trade.signal == 'long'):
            self.sell(tick.avg_buy, trade.amount)

        elif (trade.signal == 'short'):
            self.buy_back(tick, trade)

        trade.close_trade(tick, self.balance)

        return self.balance

    def execute_signal(self, signal):
        """
        Executes the signal based on its type
        """

        if(isinstance(signal, EnterMarket)):
            self.open_trade(signal.signal_type, signal.tick, signal.size)
        elif(isinstance(signal, ExitMarket)):
            self.close_trade(signal.tick, signal.trade)

    def get_open_trades(self):
        """
        Get trades that are still open
        """
        open_trades = []

        for trade in self.trades:
            if (trade.isopen):
                open_trades.append(trade)

        return open_trades

    def close_open_trades(self, last_tick):
        """
        Close open trades
        """
        open_trades = self.get_open_trades()
        for trade in open_trades:
            self.close_trade(last_tick, trade)

    def run(self):
        """
        Analyze every row of data, and open trades to apply market signals
        """

        s = self.strategy

        # Iterate on each row of data
        for index, tick in self.data.iterrows():
            tick = self.get_tick(tick['Timestamp'])
            open_trades = self.get_open_trades()
            signal = s.on_tick(tick, open_trades, self.balance)
            if(signal):
                self.execute_signal(signal)

        self.close_open_trades(tick)
        Reporter(self.balance, self.data, self.trades, self.days)

        return (self.balance.asset1 - self.balance.initial) / self.balance.initial * 100



