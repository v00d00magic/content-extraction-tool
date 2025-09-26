from Declarable.Arguments import IntArgument

class ExecutableVariable:
    def __init__(self):
        self.content = IntArgument({
            "default": 0
        })
        self.content.getResult()

    def get(self):
        return self.content.value
