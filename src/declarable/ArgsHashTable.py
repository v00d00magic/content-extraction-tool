class ArgsHashTable:
    def __init__(self):
        self.items = {}

    def add(self, name, argument):
        self.items[name] = argument

    def get(self, name, default = None):
        _out = self.items.get(name)
        if _out == None:
            return None

        if getattr(_out, "val", None) != None:
            return _out.val()
        else:
            return _out

    def __dict__(self):
        _items = {}
        for name, item in self.items.items():
            _items[name] = self.get(name)

        return _items
