import json

import ccxt
from bottle import post, hook, request, response, default_app, run

from app.config import BIT_MEX_API_KEY, BIT_MEX_API_SECRET

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
    bitmex = ccxt.bitmex({
        'apiKey': BIT_MEX_API_KEY,
        'secret': BIT_MEX_API_SECRET
    })
    if volume > 1000 and taker_side == 'sell':
        bitmex.create_limit_sell_order('BTC/USD', 10, last_price + 10)
        return {
            'data': 'sell!!'
        }

    return {
        'data': 'ok'
    }


app = default_app()

run(app, host='0.0.0.0')
