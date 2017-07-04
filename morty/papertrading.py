from morty.engine import Engine

pair = 'ETH-USD'
exchange = 'Kraken'
strategy = 'delta'
initial_balance = 1000
days = 10
depth = 2

engine = Engine(pair, exchange, strategy)
engine.backtest(initial_balance, depth, days)

