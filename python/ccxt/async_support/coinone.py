# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OnMaintenance
from ccxt.base.precise import Precise


class coinone(Exchange):

    def describe(self):
        return self.deep_extend(super(coinone, self).describe(), {
            'id': 'coinone',
            'name': 'CoinOne',
            'countries': ['KR'],  # Korea
            # 'enableRateLimit': False,
            'rateLimit': 667,
            'version': 'v2',
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createMarketOrder': None,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchClosedOrders': None,  # the endpoint that should return closed orders actually returns trades, https://github.com/ccxt/ccxt/pull/7067
                'fetchDepositAddresses': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38003300-adc12fba-323f-11e8-8525-725f53c4a659.jpg',
                'api': 'https://api.coinone.co.kr',
                'www': 'https://coinone.co.kr',
                'doc': 'https://doc.coinone.co.kr',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'api': {
                'public': {
                    'get': [
                        'orderbook/',
                        'trades/',
                        'ticker/',
                    ],
                },
                'private': {
                    'post': [
                        'account/deposit_address/',
                        'account/btc_deposit_address/',
                        'account/balance/',
                        'account/daily_balance/',
                        'account/user_info/',
                        'account/virtual_account/',
                        'order/cancel_all/',
                        'order/cancel/',
                        'order/limit_buy/',
                        'order/limit_sell/',
                        'order/complete_orders/',
                        'order/limit_orders/',
                        'order/order_info/',
                        'transaction/auth_number/',
                        'transaction/history/',
                        'transaction/krw/history/',
                        'transaction/btc/',
                        'transaction/coin/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.002,
                    'maker': 0.002,
                },
            },
            'precision': {
                'price': 4,
                'amount': 4,
                'cost': 8,
            },
            'exceptions': {
                '405': OnMaintenance,  # {"errorCode":"405","status":"maintenance","result":"error"}
                '104': OrderNotFound,  # {"errorCode":"104","errorMsg":"Order id is not exist","result":"error"}
                '108': BadSymbol,  # {"errorCode":"108","errorMsg":"Unknown CryptoCurrency","result":"error"}
                '107': BadRequest,  # {"errorCode":"107","errorMsg":"Parameter error","result":"error"}
            },
            'commonCurrencies': {
                'SOC': 'Soda Coin',
            },
        })

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for coinone
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        request = {
            'currency': 'all',
        }
        response = await self.publicGetTicker(request)
        #
        #    {
        #        "result": "success",
        #        "errorCode": "0",
        #        "timestamp": "1643676668",
        #        "xec": {
        #          "currency": "xec",
        #          "first": "0.0914",
        #          "low": "0.0894",
        #          "high": "0.096",
        #          "last": "0.0937",
        #          "volume": "1673283662.9797",
        #          "yesterday_first": "0.0929",
        #          "yesterday_low": "0.0913",
        #          "yesterday_high": "0.0978",
        #          "yesterday_last": "0.0913",
        #          "yesterday_volume": "1167285865.4571"
        #        },
        #        ...
        #    }
        #
        result = []
        quoteId = 'krw'
        quote = self.safe_currency_code(quoteId)
        baseIds = list(response.keys())
        for i in range(0, len(baseIds)):
            baseId = baseIds[i]
            ticker = self.safe_value(response, baseId, {})
            currency = self.safe_value(ticker, 'currency')
            if currency is None:
                continue
            base = self.safe_currency_code(baseId)
            result.append({
                'id': baseId,
                'symbol': base + '/' + quote,
                'base': base,
                'quote': quote,
                'settle': None,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': 'spot',
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'active': None,
                'contract': False,
                'linear': None,
                'inverse': None,
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': None,
                    'price': None,
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': ticker,
            })
        return result

    def parse_balance(self, response):
        result = {'info': response}
        balances = self.omit(response, [
            'errorCode',
            'result',
            'normalWallets',
        ])
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            balance = balances[currencyId]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'avail')
            account['total'] = self.safe_string(balance, 'balance')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostAccountBalance(params)
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = await self.publicGetOrderbook(self.extend(request, params))
        timestamp = self.safe_timestamp(response, 'timestamp')
        return self.parse_order_book(response, symbol, timestamp, 'bid', 'ask', 'price', 'qty')

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        request = {
            'currency': 'all',
            'format': 'json',
        }
        response = await self.publicGetTicker(self.extend(request, params))
        result = {}
        ids = list(response.keys())
        timestamp = self.safe_timestamp(response, 'timestamp')
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
                ticker = response[id]
                result[symbol] = self.parse_ticker(ticker, market)
                result[symbol]['timestamp'] = timestamp
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = await self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "currency":"xec",
        #         "first":"0.1069",
        #         "low":"0.09",
        #         "high":"0.1069",
        #         "last":"0.0911",
        #         "volume":"4591217267.4974",
        #         "yesterday_first":"0.1128",
        #         "yesterday_low":"0.1035",
        #         "yesterday_high":"0.1167",
        #         "yesterday_last":"0.1069",
        #         "yesterday_volume":"4014832231.5102"
        #     }
        #
        timestamp = self.safe_timestamp(ticker, 'timestamp')
        open = self.safe_string(ticker, 'first')
        last = self.safe_string(ticker, 'last')
        previousClose = self.safe_string(ticker, 'yesterday_last')
        symbol = self.safe_symbol(None, market)
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': previousClose,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }, market, False)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "timestamp": "1416893212",
        #         "price": "420000.0",
        #         "qty": "0.1",
        #         "is_ask": "1"
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "timestamp": "1416561032",
        #         "price": "419000.0",
        #         "type": "bid",
        #         "qty": "0.001",
        #         "feeRate": "-0.0015",
        #         "fee": "-0.0000015",
        #         "orderId": "E84A1AC2-8088-4FA0-B093-A3BCDB9B3C85"
        #     }
        #
        timestamp = self.safe_timestamp(trade, 'timestamp')
        market = self.safe_market(None, market)
        is_ask = self.safe_string(trade, 'is_ask')
        side = self.safe_string(trade, 'type')
        if is_ask is not None:
            if is_ask == '1':
                side = 'sell'
            elif is_ask == '0':
                side = 'buy'
        else:
            if side == 'ask':
                side = 'sell'
            elif side == 'bid':
                side = 'buy'
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'qty')
        orderId = self.safe_string(trade, 'orderId')
        feeCostString = self.safe_string(trade, 'fee')
        fee = None
        if feeCostString is not None:
            feeCostString = Precise.string_abs(feeCostString)
            feeRateString = self.safe_string(trade, 'feeRate')
            feeRateString = Precise.string_abs(feeRateString)
            feeCurrencyCode = market['quote'] if (side == 'sell') else market['base']
            fee = {
                'cost': feeCostString,
                'currency': feeCurrencyCode,
                'rate': feeRateString,
            }
        return self.safe_trade({
            'id': self.safe_string(trade, 'id'),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': orderId,
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': fee,
        }, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = await self.publicGetTrades(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "timestamp": "1416895635",
        #         "currency": "btc",
        #         "completeOrders": [
        #             {
        #                 "timestamp": "1416893212",
        #                 "price": "420000.0",
        #                 "qty": "0.1",
        #                 "is_ask": "1"
        #             }
        #         ]
        #     }
        #
        completeOrders = self.safe_value(response, 'completeOrders', [])
        return self.parse_trades(completeOrders, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' createOrder() allows limit orders only')
        await self.load_markets()
        request = {
            'price': price,
            'currency': self.market_id(symbol),
            'qty': amount,
        }
        method = 'privatePostOrder' + self.capitalize(type) + self.capitalize(side)
        response = await getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "orderId": "8a82c561-40b4-4cb3-9bc0-9ac9ffc1d63b"
        #     }
        #
        return self.parse_order(response)

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'currency': market['id'],
        }
        response = await self.privatePostOrderOrderInfo(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "status": "live",
        #         "info": {
        #             "orderId": "32FF744B-D501-423A-8BA1-05BB6BE7814A",
        #             "currency": "BTC",
        #             "type": "bid",
        #             "price": "2922000.0",
        #             "qty": "115.4950",
        #             "remainQty": "45.4950",
        #             "feeRate": "0.0003",
        #             "fee": "0",
        #             "timestamp": "1499340941"
        #         }
        #     }
        #
        info = self.safe_value(response, 'info', {})
        info['status'] = self.safe_string(info, 'status')
        return self.parse_order(info, market)

    def parse_order_status(self, status):
        statuses = {
            'live': 'open',
            'partially_filled': 'open',
            'filled': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "orderId": "8a82c561-40b4-4cb3-9bc0-9ac9ffc1d63b"
        #     }
        #
        # fetchOrder
        #
        #     {
        #         "status": "live",  # injected in fetchOrder
        #         "orderId": "32FF744B-D501-423A-8BA1-05BB6BE7814A",
        #         "currency": "BTC",
        #         "type": "bid",
        #         "price": "2922000.0",
        #         "qty": "115.4950",
        #         "remainQty": "45.4950",
        #         "feeRate": "0.0003",
        #         "fee": "0",
        #         "timestamp": "1499340941"
        #     }
        #
        # fetchOpenOrders
        #
        #     {
        #         "index": "0",
        #         "orderId": "68665943-1eb5-4e4b-9d76-845fc54f5489",
        #         "timestamp": "1449037367",
        #         "price": "444000.0",
        #         "qty": "0.3456",
        #         "type": "ask",
        #         "feeRate": "-0.0015"
        #     }
        #
        id = self.safe_string(order, 'orderId')
        priceString = self.safe_string(order, 'price')
        timestamp = self.safe_timestamp(order, 'timestamp')
        side = self.safe_string(order, 'type')
        if side == 'ask':
            side = 'sell'
        elif side == 'bid':
            side = 'buy'
        remainingString = self.safe_string(order, 'remainQty')
        amountString = self.safe_string(order, 'qty')
        status = self.safe_string(order, 'status')
        # https://github.com/ccxt/ccxt/pull/7067
        if status == 'live':
            if (remainingString is not None) and (amountString is not None):
                isLessThan = Precise.string_lt(remainingString, amountString)
                if isLessThan:
                    status = 'canceled'
        status = self.parse_order_status(status)
        symbol = None
        base = None
        quote = None
        marketId = self.safe_string_lower(order, 'currency')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                base = self.safe_currency_code(marketId)
                quote = 'KRW'
                symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
            base = market['base']
            quote = market['quote']
        fee = None
        feeCostString = self.safe_string(order, 'fee')
        if feeCostString is not None:
            feeCurrencyCode = quote if (side == 'sell') else base
            fee = {
                'cost': feeCostString,
                'rate': self.safe_string(order, 'feeRate'),
                'currency': feeCurrencyCode,
            }
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': priceString,
            'stopPrice': None,
            'cost': None,
            'average': None,
            'amount': amountString,
            'filled': None,
            'remaining': remainingString,
            'status': status,
            'fee': fee,
            'trades': None,
        }, market)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        # The returned amount might not be same as the ordered amount. If an order is partially filled, the returned amount means the remaining amount.
        # For the same reason, the returned amount and remaining are always same, and the returned filled and cost are always zero.
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOpenOrders() allows fetching closed orders with a specific symbol')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.privatePostOrderLimitOrders(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "limitOrders": [
        #             {
        #                 "index": "0",
        #                 "orderId": "68665943-1eb5-4e4b-9d76-845fc54f5489",
        #                 "timestamp": "1449037367",
        #                 "price": "444000.0",
        #                 "qty": "0.3456",
        #                 "type": "ask",
        #                 "feeRate": "-0.0015"
        #             }
        #         ]
        #     }
        #
        limitOrders = self.safe_value(response, 'limitOrders', [])
        return self.parse_orders(limitOrders, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.privatePostOrderCompleteOrders(self.extend(request, params))
        #
        # despite the name of the endpoint it returns trades which may have a duplicate orderId
        # https://github.com/ccxt/ccxt/pull/7067
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "completeOrders": [
        #             {
        #                 "timestamp": "1416561032",
        #                 "price": "419000.0",
        #                 "type": "bid",
        #                 "qty": "0.001",
        #                 "feeRate": "-0.0015",
        #                 "fee": "-0.0000015",
        #                 "orderId": "E84A1AC2-8088-4FA0-B093-A3BCDB9B3C85"
        #             }
        #         ]
        #     }
        #
        completeOrders = self.safe_value(response, 'completeOrders', [])
        return self.parse_trades(completeOrders, market, since, limit)

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            # eslint-disable-next-line quotes
            raise ArgumentsRequired(self.id + " cancelOrder() requires a symbol argument. To cancel the order, pass a symbol argument and {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument of cancelOrder.")
        price = self.safe_number(params, 'price')
        qty = self.safe_number(params, 'qty')
        isAsk = self.safe_integer(params, 'is_ask')
        if (price is None) or (qty is None) or (isAsk is None):
            # eslint-disable-next-line quotes
            raise ArgumentsRequired(self.id + " cancelOrder() requires {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument.")
        await self.load_markets()
        request = {
            'order_id': id,
            'price': price,
            'qty': qty,
            'is_ask': isAsk,
            'currency': self.market_id(symbol),
        }
        response = await self.privatePostOrderCancel(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0"
        #     }
        #
        return response

    async def fetch_deposit_addresses(self, codes=None, params={}):
        await self.load_markets()
        response = await self.privatePostAccountDepositAddress(params)
        #
        #     {
        #         result: 'success',
        #         errorCode: '0',
        #         walletAddress: {
        #             matic: null,
        #             btc: "mnobqu4i6qMCJWDpf5UimRmr8JCvZ8FLcN",
        #             xrp: null,
        #             xrp_tag: '-1',
        #             kava: null,
        #             kava_memo: null,
        #         }
        #     }
        #
        walletAddress = self.safe_value(response, 'walletAddress', {})
        keys = list(walletAddress.keys())
        result = {}
        for i in range(0, len(keys)):
            key = keys[i]
            value = walletAddress[key]
            if (not value) or (value == '-1'):
                continue
            parts = key.split('_')
            currencyId = self.safe_value(parts, 0)
            secondPart = self.safe_value(parts, 1)
            code = self.safe_currency_code(currencyId)
            depositAddress = self.safe_value(result, code)
            if depositAddress is None:
                depositAddress = {
                    'currency': code,
                    'address': None,
                    'tag': None,
                    'info': value,
                }
            address = self.safe_string(depositAddress, 'address', value)
            self.check_address(address)
            depositAddress['address'] = address
            depositAddress['info'] = address
            if (secondPart == 'tag' or secondPart == 'memo'):
                depositAddress['tag'] = value
                depositAddress['info'] = [address, value]
            result[code] = depositAddress
        return result

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/'
        if api == 'public':
            url += request
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            url += self.version + '/' + request
            nonce = str(self.nonce())
            json = self.json(self.extend({
                'access_token': self.apiKey,
                'nonce': nonce,
            }, params))
            payload = self.string_to_base64(json)
            body = self.decode(payload)
            secret = self.secret.upper()
            signature = self.hmac(payload, self.encode(secret), hashlib.sha512)
            headers = {
                'Content-Type': 'application/json',
                'X-COINONE-PAYLOAD': payload,
                'X-COINONE-SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if 'result' in response:
            result = response['result']
            if result != 'success':
                #
                #    { "errorCode": "405",  "status": "maintenance",  "result": "error"}
                #
                errorCode = self.safe_string(response, 'errorCode')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
                raise ExchangeError(feedback)
        else:
            raise ExchangeError(self.id + ' ' + body)
