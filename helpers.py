# helpers.py - general utilities
import time, json, os
def timestamp():
    return int(time.time())

def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,'w') as f:
        json.dump(obj, f, indent=2)
