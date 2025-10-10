from .ArgumentList import ArgumentList

class ApplyArgumentList(ArgumentList):
    def constructor(self):
        for item in self.items:
            item.auto_apply = True
