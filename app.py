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
        data = await websocket.receive()
        json_data = json.loads(data)
        await system.router(websocket, json_data)

@app.websocket("/ws")
async def ws():
    try:
        consumer = asyncio.create_task(receiving())
        await asyncio.gather(consumer)
    except asyncio.CancelledError:
        # Handle disconnection here
        raise

if __name__ == '__main__':
    app.run()