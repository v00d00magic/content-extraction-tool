class Response():
    def __init__(self, data):
        self.data = data
        self.check()

    @classmethod
    def convert(cls, data):
        if isinstance(data, Response):
            return data

        return cls(data)

    def check(self):
        pass

    def display(self):
        return self.data
