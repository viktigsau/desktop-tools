import json

path = 'config.json'

def get(key):
    with open(path) as f:
        data = json.load(f)
    keys = key.split('.')

    for k in keys:
        data = data[k]
    return data

def set(key, value):
    with open(path) as f:
        data = json.load(f)
    keys = key.split('.')
    last_key = keys.pop()
    new_data = data
    for k in keys:
        try:
            new_data = new_data[k]
        except KeyError:
            new_data[k] = {}
            new_data = new_data[k]
    new_data[last_key] = value
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def enshure(key, st_value=None):
    try:
        return get(key)
    except KeyError:
        set(key, st_value)
        return get(key)