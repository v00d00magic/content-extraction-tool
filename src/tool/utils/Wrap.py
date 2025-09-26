class Wrap():
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)
