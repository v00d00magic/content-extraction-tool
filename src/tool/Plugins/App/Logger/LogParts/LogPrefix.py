from Objects.Object import Object

class LogPrefix(Object):
    name: str
    id: int

    def toString(self):
        return f"{self.name}->{self.id}"
