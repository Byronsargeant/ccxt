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
    exchange = ccxt.kraken({
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_API_SECRET',
    })
    symbol = 'UNI/USD'
    side = 'buy'  # set it to 'buy' for a long position, 'sell' for a short position
    order_type = 'market'  # set it to 'market' or 'limit'
    amount = 1
    leverage = 2
    await exchange.load_markets()
    market = exchange.market(symbol)
    # if order_type is 'market', then price is not needed
    price = None
    # if order_type is 'limit', then set a price at your desired level
    # you can fetch the ticker and update price
    # const ticker = await exchange.fetchTicker (symbol);
    # const last_price = ticker['last'];
    # const ask_price = ticker['ask'];
    # const bid_price = ticker['bid'];
    # if (order_type === 'limit') {
    #     price = (side === 'buy') ? bid_price * 0.95 : ask_price * 1.05; # i.e. 5% from current price
    # }
    params = {
        'leverage': leverage,
    }
    # log
    print('Going to open a position', 'for', amount, 'worth', amount, market['base'], '~', market['settle'], 'using', side, order_type, 'order (', (exchange.price_to_precision(symbol, price) if order_type == 'limit' else ''), '), using the following params:')
    print(params)
    print('-----------------------------------------------------------------------')
    try:
        created_order = await exchange.create_order(symbol, order_type, side, amount, price, params)
        print('Created an order', created_order)
        # Fetch all your closed orders for this symbol (because we used market order)
        # - use 'fetchClosedOrders' or 'fetchOrders' and filter with 'closed' status
        all_closed_orders = await exchange.fetch_closed_orders(symbol)
        print('Fetched all your closed orders for this symbol', all_closed_orders)
        all_open_positions = await exchange.fetch_positions(symbol)
        print('Fetched all your positions for this symbol', all_open_positions)
    except Exception as e:
        print(str(e))

    await exchange.close()


asyncio.run(example())
