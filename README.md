# morty

A Python trading tool for Crypto-Trading.

![Morty](https://i.ytimg.com/vi/lZi5FaGLhCA/maxresdefault.jpg) 

**Awh man! I thought this strategy was gonna work for sure**

## TODO

- [X] Fees
- [ ] Drawdown
- [ ] Sharpe Ratio
- [ ] Graphs
- [ ] Paper trading
- [ ] Live trading
- [ ] Parameter optimizer

## Supported Pairs

### Kraken:
[[BTC, USD],
[ETH, USD],
[XRP, USD],
[BTC, EUR],
[ETH, EUR],
[XRP, EUR],
[XRP, BTC],
[ETH, BTC],
[USDT, USD]]

### Bitso:
[[BTC, MXN],
[ETH, MXN],
[XRP, MXN],
[ETH, BTC],
[XRP, BTC]]

### Poloniex
[[BTC, USDT],
[ETH, BTC],
[XRP, BTC],
[ETH, USDT],
[XRP, USDT]]

### Gemini
[[BTC, USD],
[ETH, USD]]

### Kraken:

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
