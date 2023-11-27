import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
undefined

# AUTO-TRANSPILE #
print('CCXT Version:', ccxt.version)


# ------------------------------------------------------------------------------
async def example():
    # at this moment, only OKX support embedded stop-loss & take-profit orders in unified manner. other exchanges are being added actively and will be available soon.
    exchange = ccxt.okx({
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_API_SECRET',
        'password': 'YOUR_API_PASSWORD',
    })
    symbol = 'DOGE/USDT:USDT'
    side = 'buy'  # 'buy' | 'sell'
    order_type = 'limit'  # 'market' | 'limit'
    amount = 1  # how many contracts (see `market(symbol).contractSize` to find out coin portion per one contract)
    await exchange.load_markets()
    market = exchange.market(symbol)
    ticker = await exchange.fetch_ticker(symbol)
    last_price = ticker['last']
    ask_price = ticker['ask']
    bid_price = ticker['bid']
    # if order_type is 'market', then price is not needed
    price = None
    # if order_type is 'limit', then set a price at your desired level
    if order_type == 'limit':
        price = bid_price * 0.95 if (side == 'buy') else ask_price * 1.05  # i.e. 5% from current price
    # set trigger price for stop-loss/take-profit to 2% from current price
    # (note, across different exchanges "trigger" price can be also mentioned with different synonyms, like "activation price", "stop price", "conditional price", etc. )
    stop_loss_trigger_price = (last_price if order_type == 'market' else price) * (0.98 if side == 'buy' else 1.02)
    take_profit_trigger_price = (last_price if order_type == 'market' else price) * (1.02 if side == 'buy' else 0.98)
    # when symbol's price reaches your predefined "trigger price", stop-loss order would be activated as a "market order". but if you want it to be activated as a "limit order", then set a 'price' parameter for it
    params = {
        'stopLoss': {
            'triggerPrice': stop_loss_trigger_price,
            'price': stop_loss_trigger_price * 0.98,
        },
        'takeProfit': {
            'triggerPrice': take_profit_trigger_price,
            'price': take_profit_trigger_price * 0.98,
        },
    }
    position_amount = market['contractSize'] * amount
    position_value = position_amount * last_price
    # log
    print('Going to open a position', 'for', amount, 'contracts worth', position_amount, market['base'], '~', position_value, market['settle'], 'using', side, order_type, 'order (', (exchange.price_to_precision(symbol, price) if order_type == 'limit' else ''), '), using the following params:')
    print(params)
    print('-----------------------------------------------------------------------')
    try:
        created_order = await exchange.create_order(symbol, order_type, side, amount, price, params)
        print('Created an order', created_order)
        # Fetch all your open orders for this symbol
        # - use 'fetchOpenOrders' or 'fetchOrders' and filter with 'open' status
        # - note, that some exchanges might return one order object with embedded stoploss/takeprofit fields, while other exchanges might have separate stoploss/takeprofit order objects
        all_open_orders = await exchange.fetch_open_orders(symbol)
        print('Fetched all your orders for this symbol', all_open_orders)
    except Exception as e:
        print(str(e))

    await exchange.close()


asyncio.run(example())
