# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired


class coinspot(Exchange):

    def describe(self):
        return self.deep_extend(super(coinspot, self).describe(), {
            'id': 'coinspot',
            'name': 'CoinSpot',
            'countries': ['AU'],  # Australia
            'rateLimit': 1000,
            'has': {
                'cancelOrder': None,
                'CORS': None,
                'createMarketOrder': None,
                'createOrder': True,
                'fetchBalance': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28208429-3cacdf9a-6896-11e7-854e-4c79a772a30f.jpg',
                'api': {
                    'public': 'https://www.coinspot.com.au/pubapi',
                    'private': 'https://www.coinspot.com.au/api',
                },
                'www': 'https://www.coinspot.com.au',
                'doc': 'https://www.coinspot.com.au/api',
                'referral': 'https://www.coinspot.com.au/register?code=PJURCU',
            },
            'api': {
                'public': {
                    'get': [
                        'latest',
                    ],
                },
                'private': {
                    'post': [
                        'orders',
                        'orders/history',
                        'my/coin/deposit',
                        'my/coin/send',
                        'quote/buy',
                        'quote/sell',
                        'my/balances',
                        'my/orders',
                        'my/buy',
                        'my/sell',
                        'my/buy/cancel',
                        'my/sell/cancel',
                        'ro/my/balances',
                        'ro/my/balances/{cointype}',
                        'ro/my/deposits',
                        'ro/my/withdrawals',
                        'ro/my/transactions',
                        'ro/my/transactions/{cointype}',
                        'ro/my/transactions/open',
                        'ro/my/transactions/{cointype}/open',
                        'ro/my/sendreceive',
                        'ro/my/affiliatepayments',
                        'ro/my/referralpayments',
                    ],
                },
            },
            'markets': {
                'BTC/AUD': {'id': 'btc', 'symbol': 'BTC/AUD', 'base': 'BTC', 'quote': 'AUD', 'baseId': 'btc', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'ETH/AUD': {'id': 'eth', 'symbol': 'ETH/AUD', 'base': 'ETH', 'quote': 'AUD', 'baseId': 'eth', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'XRP/AUD': {'id': 'xrp', 'symbol': 'XRP/AUD', 'base': 'XRP', 'quote': 'AUD', 'baseId': 'xrp', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'LTC/AUD': {'id': 'ltc', 'symbol': 'LTC/AUD', 'base': 'LTC', 'quote': 'AUD', 'baseId': 'ltc', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'DOGE/AUD': {'id': 'doge', 'symbol': 'DOGE/AUD', 'base': 'DOGE', 'quote': 'AUD', 'baseId': 'doge', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'RFOX/AUD': {'id': 'rfox', 'symbol': 'RFOX/AUD', 'base': 'RFOX', 'quote': 'AUD', 'baseId': 'rfox', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'POWR/AUD': {'id': 'powr', 'symbol': 'POWR/AUD', 'base': 'POWR', 'quote': 'AUD', 'baseId': 'powr', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'NEO/AUD': {'id': 'neo', 'symbol': 'NEO/AUD', 'base': 'NEO', 'quote': 'AUD', 'baseId': 'neo', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'TRX/AUD': {'id': 'trx', 'symbol': 'TRX/AUD', 'base': 'TRX', 'quote': 'AUD', 'baseId': 'trx', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'EOS/AUD': {'id': 'eos', 'symbol': 'EOS/AUD', 'base': 'EOS', 'quote': 'AUD', 'baseId': 'eos', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'XLM/AUD': {'id': 'xlm', 'symbol': 'XLM/AUD', 'base': 'XLM', 'quote': 'AUD', 'baseId': 'xlm', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'RHOC/AUD': {'id': 'rhoc', 'symbol': 'RHOC/AUD', 'base': 'RHOC', 'quote': 'AUD', 'baseId': 'rhoc', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'GAS/AUD': {'id': 'gas', 'symbol': 'GAS/AUD', 'base': 'GAS', 'quote': 'AUD', 'baseId': 'gas', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
            },
            'commonCurrencies': {
                'DRK': 'DASH',
            },
            'options': {
                'fetchBalance': 'private_post_my_balances',
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        method = self.safe_string(self.options, 'fetchBalance', 'private_post_my_balances')
        response = getattr(self, method)(params)
        #
        # read-write api keys
        #
        #     ...
        #
        # read-only api keys
        #
        #     {
        #         "status":"ok",
        #         "balances":[
        #             {
        #                 "LTC":{"balance":0.1,"audbalance":16.59,"rate":165.95}
        #             }
        #         ]
        #     }
        #
        result = {'info': response}
        balances = self.safe_value_2(response, 'balance', 'balances')
        if isinstance(balances, list):
            for i in range(0, len(balances)):
                currencies = balances[i]
                currencyIds = list(currencies.keys())
                for j in range(0, len(currencyIds)):
                    currencyId = currencyIds[j]
                    balance = currencies[currencyId]
                    code = self.safe_currency_code(currencyId)
                    account = self.account()
                    account['total'] = self.safe_string(balance, 'balance')
                    result[code] = account
        else:
            currencyIds = list(balances.keys())
            for i in range(0, len(currencyIds)):
                currencyId = currencyIds[i]
                code = self.safe_currency_code(currencyId)
                account = self.account()
                account['total'] = self.safe_string(balances, currencyId)
                result[code] = account
        return self.safe_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cointype': market['id'],
        }
        orderbook = self.privatePostOrders(self.extend(request, params))
        return self.parse_order_book(orderbook, symbol, None, 'buyorders', 'sellorders', 'rate', 'amount')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        response = self.publicGetLatest(params)
        id = self.market_id(symbol)
        id = id.lower()
        ticker = response['prices'][id]
        timestamp = self.milliseconds()
        last = self.safe_number(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_number(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cointype': market['id'],
        }
        response = self.privatePostOrdersHistory(self.extend(request, params))
        #
        #     {
        #         "status":"ok",
        #         "orders":[
        #             {"amount":0.00102091,"rate":21549.09999991,"total":21.99969168,"coin":"BTC","solddate":1604890646143,"market":"BTC/AUD"},
        #         ],
        #     }
        #
        trades = self.safe_value(response, 'orders', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # public fetchTrades
        #
        #     {
        #         "amount":0.00102091,
        #         "rate":21549.09999991,
        #         "total":21.99969168,
        #         "coin":"BTC",
        #         "solddate":1604890646143,
        #         "market":"BTC/AUD"
        #     }
        #
        priceString = self.safe_string(trade, 'rate')
        amountString = self.safe_string(trade, 'amount')
        costString = self.safe_number(trade, 'total')
        timestamp = self.safe_integer(trade, 'solddate')
        marketId = self.safe_string(trade, 'market')
        symbol = self.safe_symbol(marketId, market, '/')
        return self.safe_trade({
            'info': trade,
            'id': None,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': None,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': costString,
            'fee': None,
        }, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        method = 'privatePostMy' + self.capitalize(side)
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        request = {
            'cointype': self.market_id(symbol),
            'amount': amount,
            'rate': price,
        }
        return getattr(self, method)(self.extend(request, params))

    def cancel_order(self, id, symbol=None, params={}):
        side = self.safe_string(params, 'side')
        if side != 'buy' and side != 'sell':
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a side parameter, "buy" or "sell"')
        params = self.omit(params, 'side')
        method = 'privatePostMy' + self.capitalize(side) + 'Cancel'
        request = {
            'id': id,
        }
        return getattr(self, method)(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if not self.apiKey:
            raise AuthenticationError(self.id + ' requires apiKey for all requests')
        url = self.urls['api'][api] + '/' + path
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.json(self.extend({'nonce': nonce}, params))
            headers = {
                'Content-Type': 'application/json',
                'key': self.apiKey,
                'sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
