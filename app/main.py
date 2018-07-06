import boto3
import json
import ccxt
from app.config import BIT_MEX_API_KEY, BIT_MEX_API_SECRET
from bottle import post, hook, request, response, default_app, run

utf8 = 'utf-8'
s3 = boto3.resource('s3')
s3client = boto3.client('s3')


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
    if volume > 701 and taker_side == 'sell':
        bitmex.create_limit_sell_order('BTC/USD', {
            'amount': 10,
            'price': last_price
        })
        return {
            'data': 'sell!!'
        }

    print(data)
    return {
        'data': 'ok'
    }


app = default_app()

run(app, host='0.0.0.0')
