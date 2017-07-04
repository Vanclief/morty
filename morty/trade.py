from random import randint
from datetime import datetime
from morty.tcolors import Tcolors
from morty.balance import Balance
from morty.tick import Tick

class Trade:
    def __init__(self, signal, amount, tick, balance):
        self.id = randint(1000, 9999)
        self.signal = signal
        self.amount = amount
        self.open_tick = tick
        self.close_tick = None
        self.balance = balance
        self.isopen = True
        self.gain_p = 0
        self.profit = 0
        self.print_trade("open ")

    def get_initial_position(self):

        if (self.signal == 'long'):
            initial_position = self.open_tick.avg_buy

        elif (self.signal == 'short'):
            initial_position = self.open_tick.avg_sell

        return initial_position

    def get_final_position(self, close_tick):

        if (self.signal == 'long'):
            final_position = close_tick.avg_sell

        elif (self.signal == 'short'):
            final_position = close_tick.avg_buy

        return final_position

    def get_profit(self, close_tick):
        opening = self.get_initial_position()
        closing = self.get_final_position(close_tick)

        if (self.signal == 'long'):
            self.profit = (closing - opening) * self.amount

        elif (self.signal == 'short'):
            self.profit = (opening - closing) * self.amount

        return self.profit

    def get_gain_percent(self, close_tick):
        opening = self.get_initial_position()
        closing = self.get_final_position(close_tick)

        if (self.signal == 'long'):
            self.gain_p = (closing - opening) / opening * 100

        elif (self.signal == 'short'):
            self.gain_p = (opening - closing) / closing * 100

        return self.gain_p

    def close_trade(self, close_tick, balance):

        self.balance = balance
        self.close_tick = close_tick

        if (self.isopen):
            self.isopen = False
        else:
            print('ERROR Trade has already been closed')

        self.get_gain_percent(close_tick)
        self.get_profit(close_tick)
        self.print_trade("close")

    def print_trade(self, operation):

        tc = Tcolors()

        if (operation == 'close'):
            mid_price = self.close_tick.mid_price
            date = datetime.utcfromtimestamp(
                    self.close_tick.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        else:
            mid_price = self.open_tick.mid_price
            date = datetime.utcfromtimestamp(
                    self.open_tick.timestamp).strftime("%Y-%m-%d %H:%M:%S")

        print('ID:{0:} {1:} ${2:} {3:} {4:} #{5:} \
                %{6:} {7:} {8:} {9:} {10:} {11:} {12:} {13:}'.format(
            tc.colorize_i(tc.bold, self.id),
            tc.colorize_s(tc.header, date),
            tc.colorize_f(tc.cyan, mid_price),
            tc.polarize_s(self.signal),
            tc.polarize_s(operation),
            tc.colorize_f(tc.cyan, self.amount),
            tc.polarize_f(self.gain_p),
            tc.colorize_s(tc.bold, "|| Balance:"),
            tc.colorize_s(tc.under, self.balance.pair[1]),
            tc.colorize_f(tc.yellow, self.balance.asset1),
            tc.colorize_s(tc.under, self.balance.pair[0]),
            tc.colorize_f(tc.blue, self.balance.asset2),
            tc.colorize_s(tc.under, self.balance.pair[0] + "/Debt"),
            tc.colorize_f(tc.blue, self.balance.asset2_debt),
            ))
