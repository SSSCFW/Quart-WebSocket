from quart import Quart, render_template, websocket
from server import system
import asyncio
import json

app = Quart(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
async def hello():
    return await render_template("index.html")

async def receiving():
    while True:
        # 受け取ったデータを処理
        data = await websocket.receive()
        json_data = json.loads(data)
        await system.router(websocket, json_data)

@app.websocket("/ws")
async def ws():
    try:
        # 受け取る関数を並行実行
        system.client_websockets.add(websocket._get_current_object())
        consumer = asyncio.create_task(receiving())
        await asyncio.gather(consumer)
    except asyncio.CancelledError:
        # Handle disconnection here
        system.client_websockets.remove(websocket._get_current_object())
        raise

if __name__ == '__main__':
    app.run()