import functools

websocket_handlers = {}

def websocket(name):
    def decorator(func):
        websocket_handlers[name] = func
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator