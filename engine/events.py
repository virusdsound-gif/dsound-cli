listeners = {}

def on(event, handler):
    listeners.setdefault(event, []).append(handler)

def emit(event, data=None):
    for handler in listeners.get(event, []):
        handler(data)
