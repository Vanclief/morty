""" Backtester Command """

import sys
from morty.engine import Engine

class Backtester:

    def __init__(self, engine, initial_balance, depth, days):
        engine.set_balance(initial_balance)
        engine.backfill_data(depth, days)
        engine.run()


def main():

    args = sys.argv

    if (len(sys.argv) != 7):
        print('backtest <pair> <exchange> <strategy> <initial balance> \
                <depht> <days>')

    engine = Engine(sys.argv[1], sys.argv[2], sys.argv[3])
    bt = Backtester(engine, sys.argv[4], sys.argv[5], sys.argv[6])
