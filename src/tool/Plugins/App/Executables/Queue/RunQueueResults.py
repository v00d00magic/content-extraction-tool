class RunQueueResults():
    items: dict = {}
    iterator: int = 0

    def get(self, index: int) -> dict:
        if index < 0:
            return self.items[len(self.items.keys()) + index]

        return self.items[index]

    def set(self, iterator: int, item: dict):
        self.items[iterator] = item
