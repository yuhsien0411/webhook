from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP

app = Flask(__name__)

session = HTTP(
    testnet=False,
    api_key="OTFSXETERAKWGCFXKY",
    api_secret="WOAJELZFONJVKGINQRIIRTROQBATXFREXCFQ",
)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return 'Hello Webhook'

    if request.method == 'POST':
        data = request.get_json()

        # 顯示收到的 JSON 數據
        print("Received JSON data:", data)
        symbol = data['symbol'][0:3]+'USDT'
        side = data['side']
        if side == 'buy':
            side = 'Buy'
        else:
            side = 'Sell'
        qty = data['qty']
        
        order_result = place_order(symbol, side, qty)

        # 回傳成功訊息
        return jsonify({ 'order_result': order_result})
        # return jsonify({'symbol':symbol,'side':side,'qty':qty})

    else:
        return jsonify({'error': 'Only POST requests are supported'})

def place_order(symbol, side, qty):
    response = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Market",
        qty=qty,
    )
    return response

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, debug=True)
