import socketio
import requests

from sanic.app import Sanic
from sanic.response import html

sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app)

def get_state():
    with requests.get(f'http://127.0.0.1:9000/state') as response:
        return response.json()

global_state = None

async def background_task():
    while True:
        await sio.sleep(1)
        global_state = get_state()
        await sio.emit('state_update', global_state,
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
    global_state = get_state()
    await sio.emit('state_update', global_state,
                   namespace='/state')

app.static('/static', 'web_ui/static')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
