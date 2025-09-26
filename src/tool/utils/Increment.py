class Increment:
    def __init__(self):
        self.id = 0

    def increment(self):
        self.id += 1

    def getIndex(self):
        self.increment()

        return self.id

    def null(self):
        self.id = 0
