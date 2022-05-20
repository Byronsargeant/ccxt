<?php

namespace ccxt\async;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use \ccxt\ExchangeError;
use \ccxt\ArgumentsRequired;
use \ccxt\OrderNotFound;

class bitflyer extends Exchange {

    public function describe() {
        return $this->deep_extend(parent::describe (), array(
            'id' => 'bitflyer',
            'name' => 'bitFlyer',
            'countries' => array( 'JP' ),
            'version' => 'v1',
            'rateLimit' => 1000, // their nonce-timestamp is in seconds...
            'hostname' => 'bitflyer.com', // or bitflyer.com
            'has' => array(
                'CORS' => null,
                'spot' => true,
                'margin' => false,
                'swap' => null, // has but not fully implemented
                'future' => null, // has but not fully implemented
                'option' => false,
                'cancelOrder' => true,
                'createOrder' => true,
                'fetchBalance' => true,
                'fetchClosedOrders' => 'emulated',
                'fetchDeposits' => true,
                'fetchMarkets' => true,
                'fetchMyTrades' => true,
                'fetchOpenOrders' => 'emulated',
                'fetchOrder' => 'emulated',
                'fetchOrderBook' => true,
                'fetchOrders' => true,
                'fetchPositions' => true,
                'fetchTicker' => true,
                'fetchTrades' => true,
                'fetchTradingFee' => true,
                'fetchTradingFees' => false,
                'fetchTransfer' => false,
                'fetchTransfers' => false,
                'fetchWithdrawals' => true,
                'transfer' => false,
                'withdraw' => true,
            ),
            'urls' => array(
                'logo' => 'https://user-images.githubusercontent.com/1294454/28051642-56154182-660e-11e7-9b0d-6042d1e6edd8.jpg',
                'api' => 'https://api.{hostname}',
                'www' => 'https://bitflyer.com',
                'doc' => 'https://lightning.bitflyer.com/docs?lang=en',
            ),
            'api' => array(
                'public' => array(
                    'get' => array(
                        'getmarkets/usa', // new (wip)
                        'getmarkets/eu',  // new (wip)
                        'getmarkets',     // or 'markets'
                        'getboard',       // ...
                        'getticker',
                        'getexecutions',
                        'gethealth',
                        'getboardstate',
                        'getchats',
                    ),
                ),
                'private' => array(
                    'get' => array(
                        'getpermissions',
                        'getbalance',
                        'getbalancehistory',
                        'getcollateral',
                        'getcollateralhistory',
                        'getcollateralaccounts',
                        'getaddresses',
                        'getcoinins',
                        'getcoinouts',
                        'getbankaccounts',
                        'getdeposits',
                        'getwithdrawals',
                        'getchildorders',
                        'getparentorders',
                        'getparentorder',
                        'getexecutions',
                        'getpositions',
                        'gettradingcommission',
                    ),
                    'post' => array(
                        'sendcoin',
                        'withdraw',
                        'sendchildorder',
                        'cancelchildorder',
                        'sendparentorder',
                        'cancelparentorder',
                        'cancelallchildorders',
                    ),
                ),
            ),
            'fees' => array(
                'trading' => array(
                    'maker' => $this->parse_number('0.002'),
                    'taker' => $this->parse_number('0.002'),
                ),
            ),
        ));
    }

    public function parse_expiry_date($expiry) {
        $day = mb_substr($expiry, 0, 2 - 0);
        $monthName = mb_substr($expiry, 2, 5 - 2);
        $year = mb_substr($expiry, 5, 9 - 5);
        $months = array(
            'JAN' => '01',
            'FEB' => '02',
            'MAR' => '03',
            'APR' => '04',
            'MAY' => '05',
            'JUN' => '06',
            'JUL' => '07',
            'AUG' => '08',
            'SEP' => '09',
            'OCT' => '10',
            'NOV' => '11',
            'DEC' => '12',
        );
        $month = $this->safe_string($months, $monthName);
        return $this->parse8601($year . '-' . $month . '-' . $day . 'T00:00:00Z');
    }

    public function fetch_markets($params = array ()) {
        /**
         * retrieves data on all $markets for bitflyer
         * @param {dict} $params extra parameters specific to the exchange api endpoint
         * @return {[dict]} an array of objects representing $market data
         */
        $jp_markets = yield $this->publicGetGetmarkets ($params);
        //
        //     array(
        //         // $spot
        //         array( "product_code" => "BTC_JPY", "market_type" => "Spot" ),
        //         array( "product_code" => "BCH_BTC", "market_type" => "Spot" ),
        //         // forex $swap
        //         array( "product_code" => "FX_BTC_JPY", "market_type" => "FX" ),
        //         // $future
        //         array(
        //             "product_code" => "BTCJPY11FEB2022",
        //             "alias" => "BTCJPY_MAT1WK",
        //             "market_type" => "Futures",
        //         ),
        //     );
        //
        $us_markets = yield $this->publicGetGetmarketsUsa ($params);
        //
        //     array(
        //         array( "product_code" => "BTC_USD", "market_type" => "Spot" ),
        //         array( "product_code" => "BTC_JPY", "market_type" => "Spot" ),
        //     );
        //
        $eu_markets = yield $this->publicGetGetmarketsEu ($params);
        //
        //     array(
        //         array( "product_code" => "BTC_EUR", "market_type" => "Spot" ),
        //         array( "product_code" => "BTC_JPY", "market_type" => "Spot" ),
        //     );
        //
        $markets = $this->array_concat($jp_markets, $us_markets);
        $markets = $this->array_concat($markets, $eu_markets);
        $result = array();
        for ($i = 0; $i < count($markets); $i++) {
            $market = $markets[$i];
            $id = $this->safe_string($market, 'product_code');
            $currencies = explode('_', $id);
            $marketType = $this->safe_string($market, 'market_type');
            $swap = ($marketType === 'FX');
            $future = ($marketType === 'Futures');
            $spot = !$swap && !$future;
            $type = 'spot';
            $settle = null;
            $baseId = null;
            $quoteId = null;
            $expiry = null;
            if ($spot) {
                $baseId = $this->safe_string($currencies, 0);
                $quoteId = $this->safe_string($currencies, 1);
            } else if ($swap) {
                $type = 'swap';
                $baseId = $this->safe_string($currencies, 1);
                $quoteId = $this->safe_string($currencies, 2);
            } else if ($future) {
                $alias = $this->safe_string($market, 'alias');
                if ($alias === null) {
                    // no $alias:
                    // array( product_code => 'BTCJPY11MAR2022', market_type => 'Futures' )
                    // TODO this will break if there are products with 4 chars
                    $baseId = mb_substr($id, 0, 3 - 0);
                    $quoteId = mb_substr($id, 3, 6 - 3);
                    // last 9 chars are $expiry date
                    $expiryDate = mb_substr($id, -9);
                    $expiry = $this->parse_expiry_date($expiryDate);
                } else {
                    $splitAlias = explode('_', $alias);
                    $currencyIds = $this->safe_string($splitAlias, 0);
                    $baseId = mb_substr($currencyIds, 0, -3 - 0);
                    $quoteId = mb_substr($currencyIds, -3);
                    $splitId = explode($currencyIds, $id);
                    $expiryDate = $this->safe_string($splitId, 1);
                    $expiry = $this->parse_expiry_date($expiryDate);
                }
                $type = 'future';
            }
            $base = $this->safe_currency_code($baseId);
            $quote = $this->safe_currency_code($quoteId);
            $symbol = $base . '/' . $quote;
            $taker = $this->fees['trading']['taker'];
            $maker = $this->fees['trading']['maker'];
            $contract = $swap || $future;
            if ($contract) {
                $maker = 0.0;
                $taker = 0.0;
                $settle = 'JPY';
                $symbol = $symbol . ':' . $settle;
                if ($future) {
                    $symbol = $symbol . '-' . $this->yymmdd($expiry);
                }
            }
            $result[] = array(
                'id' => $id,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'settle' => $settle,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'settleId' => null,
                'type' => $type,
                'spot' => $spot,
                'margin' => false,
                'swap' => $swap,
                'future' => $future,
                'option' => false,
                'active' => true,
                'contract' => $contract,
                'linear' => $spot ? null : true,
                'inverse' => $spot ? null : false,
                'taker' => $taker,
                'maker' => $maker,
                'contractSize' => null,
                'expiry' => $expiry,
                'expiryDatetime' => $this->iso8601($expiry),
                'strike' => null,
                'optionType' => null,
                'precision' => array(
                    'amount' => null,
                    'price' => null,
                ),
                'limits' => array(
                    'leverage' => array(
                        'min' => null,
                        'max' => null,
                    ),
                    'amount' => array(
                        'min' => null,
                        'max' => null,
                    ),
                    'price' => array(
                        'min' => null,
                        'max' => null,
                    ),
                    'cost' => array(
                        'min' => null,
                        'max' => null,
                    ),
                ),
                'info' => $market,
            );
        }
        return $result;
    }

    public function parse_balance($response) {
        $result = array( 'info' => $response );
        for ($i = 0; $i < count($response); $i++) {
            $balance = $response[$i];
            $currencyId = $this->safe_string($balance, 'currency_code');
            $code = $this->safe_currency_code($currencyId);
            $account = $this->account();
            $account['total'] = $this->safe_string($balance, 'amount');
            $account['free'] = $this->safe_string($balance, 'available');
            $result[$code] = $account;
        }
        return $this->safe_balance($result);
    }

    public function fetch_balance($params = array ()) {
        yield $this->load_markets();
        $response = yield $this->privateGetGetbalance ($params);
        //
        //     array(
        //         array(
        //             "currency_code" => "JPY",
        //             "amount" => 1024078,
        //             "available" => 508000
        //         ),
        //         array(
        //             "currency_code" => "BTC",
        //             "amount" => 10.24,
        //             "available" => 4.12
        //         ),
        //         {
        //             "currency_code" => "ETH",
        //             "amount" => 20.48,
        //             "available" => 16.38
        //         }
        //     )
        //
        return $this->parse_balance($response);
    }

    public function fetch_order_book($symbol, $limit = null, $params = array ()) {
        yield $this->load_markets();
        $request = array(
            'product_code' => $this->market_id($symbol),
        );
        $orderbook = yield $this->publicGetGetboard (array_merge($request, $params));
        return $this->parse_order_book($orderbook, $symbol, null, 'bids', 'asks', 'price', 'size');
    }

    public function parse_ticker($ticker, $market = null) {
        $symbol = $this->safe_symbol(null, $market);
        $timestamp = $this->parse8601($this->safe_string($ticker, 'timestamp'));
        $last = $this->safe_string($ticker, 'ltp');
        return $this->safe_ticker(array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'high' => null,
            'low' => null,
            'bid' => $this->safe_string($ticker, 'best_bid'),
            'bidVolume' => null,
            'ask' => $this->safe_string($ticker, 'best_ask'),
            'askVolume' => null,
            'vwap' => null,
            'open' => null,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => null,
            'percentage' => null,
            'average' => null,
            'baseVolume' => $this->safe_string($ticker, 'volume_by_product'),
            'quoteVolume' => null,
            'info' => $ticker,
        ), $market, false);
    }

    public function fetch_ticker($symbol, $params = array ()) {
        yield $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'product_code' => $market['id'],
        );
        $response = yield $this->publicGetGetticker (array_merge($request, $params));
        return $this->parse_ticker($response, $market);
    }

    public function parse_trade($trade, $market = null) {
        //
        // fetchTrades (public) v1
        //
        //     {
        //          "id":2278466664,
        //          "side":"SELL",
        //          "price":56810.7,
        //          "size":0.08798,
        //          "exec_date":"2021-11-19T11:46:39.323",
        //          "buy_child_order_acceptance_id":"JRF20211119-114209-236525",
        //          "sell_child_order_acceptance_id":"JRF20211119-114639-236919"
        //      }
        //
        //      {
        //          "id":2278463423,
        //          "side":"BUY",
        //          "price":56757.83,
        //          "size":0.6003,"exec_date":"2021-11-19T11:28:00.523",
        //          "buy_child_order_acceptance_id":"JRF20211119-112800-236526",
        //          "sell_child_order_acceptance_id":"JRF20211119-112734-062017"
        //      }
        //
        //
        //
        $side = $this->safe_string_lower($trade, 'side');
        if ($side !== null) {
            if (strlen($side) < 1) {
                $side = null;
            }
        }
        $order = null;
        if ($side !== null) {
            $id = $side . '_child_order_acceptance_id';
            if (is_array($trade) && array_key_exists($id, $trade)) {
                $order = $trade[$id];
            }
        }
        if ($order === null) {
            $order = $this->safe_string($trade, 'child_order_acceptance_id');
        }
        $timestamp = $this->parse8601($this->safe_string($trade, 'exec_date'));
        $priceString = $this->safe_string($trade, 'price');
        $amountString = $this->safe_string($trade, 'size');
        $id = $this->safe_string($trade, 'id');
        $market = $this->safe_market(null, $market);
        return $this->safe_trade(array(
            'id' => $id,
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'symbol' => $market['symbol'],
            'order' => $order,
            'type' => null,
            'side' => $side,
            'takerOrMaker' => null,
            'price' => $priceString,
            'amount' => $amountString,
            'cost' => null,
            'fee' => null,
        ), $market);
    }

    public function fetch_trades($symbol, $since = null, $limit = null, $params = array ()) {
        yield $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'product_code' => $market['id'],
        );
        $response = yield $this->publicGetGetexecutions (array_merge($request, $params));
        return $this->parse_trades($response, $market, $since, $limit);
    }

    public function fetch_trading_fee($symbol, $params = array ()) {
        yield $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'product_code' => $market['id'],
        );
        $response = yield $this->privateGetGettradingcommission (array_merge($request, $params));
        //
        //   {
        //       commission_rate => '0.0020'
        //   }
        //
        $fee = $this->safe_number($response, 'commission_rate');
        return array(
            'info' => $response,
            'symbol' => $symbol,
            'maker' => $fee,
            'taker' => $fee,
        );
    }

    public function create_order($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        yield $this->load_markets();
        $request = array(
            'product_code' => $this->market_id($symbol),
            'child_order_type' => strtoupper($type),
            'side' => strtoupper($side),
            'price' => $price,
            'size' => $amount,
        );
        $result = yield $this->privatePostSendchildorder (array_merge($request, $params));
        // array( "status" => - 200, "error_message" => "Insufficient funds", "data" => null )
        $id = $this->safe_string($result, 'child_order_acceptance_id');
        return array(
            'info' => $result,
            'id' => $id,
        );
    }

    public function cancel_order($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' cancelOrder() requires a `$symbol` argument');
        }
        yield $this->load_markets();
        $request = array(
            'product_code' => $this->market_id($symbol),
            'child_order_acceptance_id' => $id,
        );
        return yield $this->privatePostCancelchildorder (array_merge($request, $params));
    }

    public function parse_order_status($status) {
        $statuses = array(
            'ACTIVE' => 'open',
            'COMPLETED' => 'closed',
            'CANCELED' => 'canceled',
            'EXPIRED' => 'canceled',
            'REJECTED' => 'canceled',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_order($order, $market = null) {
        $timestamp = $this->parse8601($this->safe_string($order, 'child_order_date'));
        $price = $this->safe_string($order, 'price');
        $amount = $this->safe_string($order, 'size');
        $filled = $this->safe_string($order, 'executed_size');
        $remaining = $this->safe_string($order, 'outstanding_size');
        $status = $this->parse_order_status($this->safe_string($order, 'child_order_state'));
        $type = $this->safe_string_lower($order, 'child_order_type');
        $side = $this->safe_string_lower($order, 'side');
        $marketId = $this->safe_string($order, 'product_code');
        $symbol = $this->safe_symbol($marketId, $market);
        $fee = null;
        $feeCost = $this->safe_number($order, 'total_commission');
        if ($feeCost !== null) {
            $fee = array(
                'cost' => $feeCost,
                'currency' => null,
                'rate' => null,
            );
        }
        $id = $this->safe_string($order, 'child_order_acceptance_id');
        return $this->safe_order(array(
            'id' => $id,
            'clientOrderId' => null,
            'info' => $order,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'lastTradeTimestamp' => null,
            'status' => $status,
            'symbol' => $symbol,
            'type' => $type,
            'timeInForce' => null,
            'postOnly' => null,
            'side' => $side,
            'price' => $price,
            'stopPrice' => null,
            'cost' => null,
            'amount' => $amount,
            'filled' => $filled,
            'remaining' => $remaining,
            'fee' => $fee,
            'average' => null,
            'trades' => null,
        ), $market);
    }

    public function fetch_orders($symbol = null, $since = null, $limit = 100, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' fetchOrders() requires a `$symbol` argument');
        }
        yield $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'product_code' => $market['id'],
            'count' => $limit,
        );
        $response = yield $this->privateGetGetchildorders (array_merge($request, $params));
        $orders = $this->parse_orders($response, $market, $since, $limit);
        if ($symbol !== null) {
            $orders = $this->filter_by($orders, 'symbol', $symbol);
        }
        return $orders;
    }

    public function fetch_open_orders($symbol = null, $since = null, $limit = 100, $params = array ()) {
        $request = array(
            'child_order_state' => 'ACTIVE',
        );
        return yield $this->fetch_orders($symbol, $since, $limit, array_merge($request, $params));
    }

    public function fetch_closed_orders($symbol = null, $since = null, $limit = 100, $params = array ()) {
        $request = array(
            'child_order_state' => 'COMPLETED',
        );
        return yield $this->fetch_orders($symbol, $since, $limit, array_merge($request, $params));
    }

    public function fetch_order($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' fetchOrder() requires a `$symbol` argument');
        }
        $orders = yield $this->fetch_orders($symbol);
        $ordersById = $this->index_by($orders, 'id');
        if (is_array($ordersById) && array_key_exists($id, $ordersById)) {
            return $ordersById[$id];
        }
        throw new OrderNotFound($this->id . ' No order found with $id ' . $id);
    }

    public function fetch_my_trades($symbol = null, $since = null, $limit = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' fetchMyTrades() requires a `$symbol` argument');
        }
        yield $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'product_code' => $market['id'],
        );
        if ($limit !== null) {
            $request['count'] = $limit;
        }
        $response = yield $this->privateGetGetexecutions (array_merge($request, $params));
        return $this->parse_trades($response, $market, $since, $limit);
    }

    public function fetch_positions($symbols = null, $params = array ()) {
        if ($symbols === null) {
            throw new ArgumentsRequired($this->id . ' fetchPositions() requires a `$symbols` argument, exactly one symbol in an array');
        }
        yield $this->load_markets();
        $request = array(
            'product_code' => $this->market_ids($symbols),
        );
        $response = yield $this->privateGetpositions (array_merge($request, $params));
        //
        //     array(
        //         {
        //             "product_code" => "FX_BTC_JPY",
        //             "side" => "BUY",
        //             "price" => 36000,
        //             "size" => 10,
        //             "commission" => 0,
        //             "swap_point_accumulate" => -35,
        //             "require_collateral" => 120000,
        //             "open_date" => "2015-11-03T10:04:45.011",
        //             "leverage" => 3,
        //             "pnl" => 965,
        //             "sfd" => -0.5
        //         }
        //     )
        //
        // todo unify parsePosition/parsePositions
        return $response;
    }

    public function withdraw($code, $amount, $address, $tag = null, $params = array ()) {
        $this->check_address($address);
        yield $this->load_markets();
        if ($code !== 'JPY' && $code !== 'USD' && $code !== 'EUR') {
            throw new ExchangeError($this->id . ' allows withdrawing JPY, USD, EUR only, ' . $code . ' is not supported');
        }
        $currency = $this->currency($code);
        $request = array(
            'currency_code' => $currency['id'],
            'amount' => $amount,
            // 'bank_account_id' => 1234,
        );
        $response = yield $this->privatePostWithdraw (array_merge($request, $params));
        //
        //     {
        //         "message_id" => "69476620-5056-4003-bcbe-42658a2b041b"
        //     }
        //
        return $this->parse_transaction($response, $currency);
    }

    public function fetch_deposits($code = null, $since = null, $limit = null, $params = array ()) {
        yield $this->load_markets();
        $currency = null;
        $request = array();
        if ($code !== null) {
            $currency = $this->currency($code);
        }
        if ($limit !== null) {
            $request['count'] = $limit; // default 100
        }
        $response = yield $this->privateGetGetcoinins (array_merge($request, $params));
        //
        //     array(
        //         {
        //             "id" => 100,
        //             "order_id" => "CDP20151227-024141-055555",
        //             "currency_code" => "BTC",
        //             "amount" => 0.00002,
        //             "address" => "1WriteySQufKZ2pVuM1oMhPrTtTVFq35j",
        //             "tx_hash" => "9f92ee65a176bb9545f7becb8706c50d07d4cee5ffca34d8be3ef11d411405ae",
        //             "status" => "COMPLETED",
        //             "event_date" => "2015-11-27T08:59:20.301"
        //         }
        //     )
        //
        return $this->parse_transactions($response, $currency, $since, $limit);
    }

    public function fetch_withdrawals($code = null, $since = null, $limit = null, $params = array ()) {
        yield $this->load_markets();
        $currency = null;
        $request = array();
        if ($code !== null) {
            $currency = $this->currency($code);
        }
        if ($limit !== null) {
            $request['count'] = $limit; // default 100
        }
        $response = yield $this->privateGetGetcoinouts (array_merge($request, $params));
        //
        //     array(
        //         {
        //             "id" => 500,
        //             "order_id" => "CWD20151224-014040-077777",
        //             "currency_code" => "BTC",
        //             "amount" => 0.1234,
        //             "address" => "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        //             "tx_hash" => "724c07dfd4044abcb390b0412c3e707dd5c4f373f0a52b3bd295ce32b478c60a",
        //             "fee" => 0.0005,
        //             "additional_fee" => 0.0001,
        //             "status" => "COMPLETED",
        //             "event_date" => "2015-12-24T01:40:40.397"
        //         }
        //     )
        //
        return $this->parse_transactions($response, $currency, $since, $limit);
    }

    public function parse_deposit_status($status) {
        $statuses = array(
            'PENDING' => 'pending',
            'COMPLETED' => 'ok',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_withdrawal_status($status) {
        $statuses = array(
            'PENDING' => 'pending',
            'COMPLETED' => 'ok',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_transaction($transaction, $currency = null) {
        //
        // fetchDeposits
        //
        //     {
        //         "id" => 100,
        //         "order_id" => "CDP20151227-024141-055555",
        //         "currency_code" => "BTC",
        //         "amount" => 0.00002,
        //         "address" => "1WriteySQufKZ2pVuM1oMhPrTtTVFq35j",
        //         "tx_hash" => "9f92ee65a176bb9545f7becb8706c50d07d4cee5ffca34d8be3ef11d411405ae",
        //         "status" => "COMPLETED",
        //         "event_date" => "2015-11-27T08:59:20.301"
        //     }
        //
        // fetchWithdrawals
        //
        //     {
        //         "id" => 500,
        //         "order_id" => "CWD20151224-014040-077777",
        //         "currency_code" => "BTC",
        //         "amount" => 0.1234,
        //         "address" => "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        //         "tx_hash" => "724c07dfd4044abcb390b0412c3e707dd5c4f373f0a52b3bd295ce32b478c60a",
        //         "fee" => 0.0005,
        //         "additional_fee" => 0.0001,
        //         "status" => "COMPLETED",
        //         "event_date" => "2015-12-24T01:40:40.397"
        //     }
        //
        // withdraw
        //
        //     {
        //         "message_id" => "69476620-5056-4003-bcbe-42658a2b041b"
        //     }
        //
        $id = $this->safe_string_2($transaction, 'id', 'message_id');
        $address = $this->safe_string($transaction, 'address');
        $currencyId = $this->safe_string($transaction, 'currency_code');
        $code = $this->safe_currency_code($currencyId, $currency);
        $timestamp = $this->parse8601($this->safe_string($transaction, 'event_date'));
        $amount = $this->safe_number($transaction, 'amount');
        $txId = $this->safe_string($transaction, 'tx_hash');
        $rawStatus = $this->safe_string($transaction, 'status');
        $type = null;
        $status = null;
        $fee = null;
        if (is_array($transaction) && array_key_exists('fee', $transaction)) {
            $type = 'withdrawal';
            $status = $this->parse_withdrawal_status($rawStatus);
            $feeCost = $this->safe_number($transaction, 'fee');
            $additionalFee = $this->safe_number($transaction, 'additional_fee');
            $fee = array( 'currency' => $code, 'cost' => $feeCost . $additionalFee );
        } else {
            $type = 'deposit';
            $status = $this->parse_deposit_status($rawStatus);
        }
        return array(
            'info' => $transaction,
            'id' => $id,
            'txid' => $txId,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'network' => null,
            'address' => $address,
            'addressTo' => $address,
            'addressFrom' => null,
            'tag' => null,
            'tagTo' => null,
            'tagFrom' => null,
            'type' => $type,
            'amount' => $amount,
            'currency' => $code,
            'status' => $status,
            'updated' => null,
            'internal' => null,
            'fee' => $fee,
        );
    }

    public function sign($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $request = '/' . $this->version . '/';
        if ($api === 'private') {
            $request .= 'me/';
        }
        $request .= $path;
        if ($method === 'GET') {
            if ($params) {
                $request .= '?' . $this->urlencode($params);
            }
        }
        $baseUrl = $this->implode_hostname($this->urls['api']);
        $url = $baseUrl . $request;
        if ($api === 'private') {
            $this->check_required_credentials();
            $nonce = (string) $this->nonce();
            $auth = implode('', array($nonce, $method, $request));
            if ($params) {
                if ($method !== 'GET') {
                    $body = $this->json($params);
                    $auth .= $body;
                }
            }
            $headers = array(
                'ACCESS-KEY' => $this->apiKey,
                'ACCESS-TIMESTAMP' => $nonce,
                'ACCESS-SIGN' => $this->hmac($this->encode($auth), $this->encode($this->secret)),
                'Content-Type' => 'application/json',
            );
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }
}
