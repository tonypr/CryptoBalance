import asyncio
import socketio

from cryptobalance import CryptoBalance
crypto_balance = CryptoBalance("config")
crypto_balance.update()

from sanic.app import Sanic
from sanic.response import json

sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app)

async def background_task():
    while True:
        await sio.sleep(1)
        crypto_balance.update()

@app.listener('before_server_start')
def before_server_start(sanic, loop):
    sio.start_background_task(background_task)

@app.route('/state')
async def state(request):
    return json({'data': crypto_balance.state()})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)
