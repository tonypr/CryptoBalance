import asyncio
import socketio

from cryptobalance import CryptoBalance
crypto_balance = CryptoBalance("config")
crypto_balance.update()

from sanic.app import Sanic
from sanic.response import html

sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app)

async def background_task():
    while True:
        await sio.sleep(0.01)
        crypto_balance.update()
        await sio.emit('state_update', {'data': crypto_balance.state()},
                       namespace='/state')

@app.listener('before_server_start')
def before_server_start(sanic, loop):
    sio.start_background_task(background_task)

@app.route('/')
async def index(request):
    with open('web_ui/templates/index.html') as f:
        return html(f.read())

@sio.on('connect', namespace='/state')
async def test_connect(sid, environ):
    await sio.emit('state_update', {'data': crypto_balance.state()},
                   namespace='/state')

app.static('/static', 'web_ui/static')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
