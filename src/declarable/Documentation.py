class Documentation:
    def __init__(self):
        self.keys = {}

    def loadKey(self, key_name, key_item):
        self.keys[key_name] = key_item

    def loadKeys(self, keys):
        for key_name, key_item in keys.items():
            self.loadKey(key_name, key_item)

    def get(self, key_name):
        _key = self.keys.get(key_name)
        if _key == None:
            return {
                "en_US": "@"+key_name
            }

        return _key

documentation = Documentation()
