import json

class Config:
    def __init__(self, path: str='config.json'):
        self.path = path

    def get(self, key):
        with open(self.path) as f:
            data = json.load(f)
        keys = key.split('.')

        for k in keys:
            data = data[k]
        return data

    def set(self, key, value):
        with open(self.path) as f:
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
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def enshure(self, key, st_value=None):
        try:
            return self.get(key)
        except KeyError:
            set(key, st_value)
            return self.get(key)