from quart import Quart, render_template, websocket
from server import dec
import json

client_websockets = set()

async def router(ws, data):
    try:
        func_name = data.get("type", "")
        handler = dec.websocket_handlers.get(func_name)
        if handler and callable(handler):
            await handler(ws, data)
        else:
            print(f"Function {func_name} not found or not callable.")
    except Exception as e:
        print(f"Error in router: {e}")
        await ws.send(json.dumps({"error": str(e)}))

def response_data(data, response):
    response["type"] = data.get("type", "")
    return str(json.dumps(response))

async def broadcast(data):
    for ws in client_websockets:
        await ws.send(data)

@dec.websocket("send_message")
async def send_message(ws, data):
    message = data.get("message", "")
    await broadcast(response_data(data, {"message": message}))
    # await ws.send(response_data(data, {"message": message}))

