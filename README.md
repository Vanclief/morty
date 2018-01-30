# morty

A Python trading tool for Crypto-Trading.

![Morty](https://fsmedia.imgix.net/ff/7a/27/d6/5afc/474d/8567/4bfbfc596f6c/would-morty-like-big-bang-theory.png?auto=format%2Ccompress&w=700) 

**Awh man! I thought this strategy was gonna work for sure**

*Disclamer*: This project is abdandoned. It worked as a very simple backtester for crypto trading, you can modify the Backfiller to use public data from Bitfinex, but honestly you are better using [Catalyst](https://github.com/enigmampc/catalyst). 

## TODO

- [X] Fees
- [ ] Drawdown
- [ ] Sharpe Ratio
- [ ] Graphs
- [ ] Paper trading
- [ ] Live trading
- [ ] Parameter optimizer

## Setup

`git clone https://github.com/Vanclief/morty.git`

`python3 setup.py develop`

## Backtesting

`backtest <pair> <exchange> <strategy> <initial balance> <depht> <days>`

### Parameters:

*Pair:* Slash separated symbols, see specific exchange .
*Exchange:* Name of the exchange.
*Strategy:* Name of the strategy file.
*Initial Balance:* Starting balance
*Depth:* Depth for the average buy / sell.
*Days:* Backward number of days range.

## Papertrading

WIP

## Livetrading

WIP
