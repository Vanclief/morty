from morty.tcolors import Tcolors

tc = Tcolors()

class Reporter():

    def __init__(self, balance, data, trades, days):
        print ('=============================')
        self.balance = balance
        self.data = data
        self.trades = trades
        self.days = days
        self.print_end_balance(self.balance.asset1, self.balance.initial)
        self.print_buy_hold()
        self.print_vs_buy_hold(self.balance.asset1)
        self.print_trade_info()

    def calc_buy_hold(self):
        """
        Calculate the result of buying and holding
        """
        hold_coins = float(self.balance.initial) / float(self.data.iloc[0]['Avg_Buy'])
        return hold_coins * float(self.data.iloc[-1]['Avg_Sell'])


    def print_end_balance(self, balance, initial_balance):
        # Calculate delta with initial balance
        p_profit = (balance - initial_balance) / initial_balance * 100
        b = tc.colorize_f(tc.bold, balance)

        if (p_profit > 0):
            p = tc.colorize_f(tc.green, p_profit)
        else:
            p = tc.colorize_f(tc.red, p_profit)

        print ('End balance: {:s} %{:s}'.format(b, p))

    def print_buy_hold(self):
        hold_balance = self.calc_buy_hold()
        p_delta = tc.polarize_f((hold_balance - self.balance.initial) /
                self.balance.initial * 100)
        balance = tc.colorize_f(tc.bold, hold_balance)
        print ('Buy & Hold : {:} %{:}'.format(balance, p_delta))

    def print_vs_buy_hold(self, balance):
        hold_balance = self.calc_buy_hold()
        vs_hold =  tc.polarize_f((balance - hold_balance ) / hold_balance * 100)
        print ('vs buy & hold: %{:}'.format(vs_hold))

    def print_trade_info(self):
        win = 0
        loss = 0
        for trade in self.trades:
            if (trade.profit > 0):
                win += 1
            else:
                loss += 1

        trades = tc.colorize_i(tc.bold, len(self.trades))
        days = tc.colorize_i(tc.bold, self.days)
        rate = tc.colorize_f(tc.red, (loss / (win + loss) * 100))
        print ('{:} trades in {:} day(s) '.format(trades, days))
        print ('Win/Loss: {:}/{:}'.format(win, loss))
        print ('Error rate: %{:}'.format(rate))

    def plot(self):
        """ Plot the data """

        print('Plotting the data')


