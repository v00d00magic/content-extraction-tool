class Wrap():
    def __init_subclass__(cls):
        cls._keys = []

        _vars = vars(cls)
        _annotations = _vars.get("__annotations__")

        if _annotations != None:
            for name, val in _annotations.items():
                cls._keys.append(name)

        cls._name = _vars.get("__module__")

    def __init__(self, data):
        for key, val in data.items():
            if key == "_keys":
                continue

            if hasattr(self, key) == True:
                setattr(self, key, val)

    @classmethod
    def getStructure(cls):
        return {
            "wrap": {
                "name": cls._name,
                "keys": cls._keys
            }
        }

    def toJson(self):
        payload = {}

        for key in self._keys:
            payload[key] = getattr(self, key, None)

        return payload
