import json

import ccxt
import requests
from bottle import post, hook, request, response, default_app, run

from app.config import BITBANK_API_KEY, BITBANK_API_SECRET

utf8 = 'utf-8'


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@post('/')
def inago():
    data = json.loads(request.body.read().decode(utf8))
    board_name = data['boardName']
    taker_side = data['takerSide']
    volume = data['volume']
    last_price = data['lastPrice']
    pair_currency = data['pairCurrency']
    from_unix_time = data['fromUnixTime']
    to_unix_time = data['toUnixTime']
    bitbank = ccxt.bitbank({
        'apiKey': BITBANK_API_KEY,
        'secret': BITBANK_API_SECRET
    })
    bitbank_last_price = int(requests.get('https://public.bitbank.cc/btc_jpy/ticker').json()['data']['last'])
    if volume > 1000 and taker_side == 'buy':
        bitbank.create_limit_buy_order('BTC/JPY', 0.001, bitbank_last_price - 500)
        return {
            'data': 'buy!!'
        }

    return {
        'data': 'ok'
    }


app = default_app()

run(app, host='0.0.0.0')
