from Executables.Variables.ExecutableVariable import ExecutableVariable
from Declarable.Arguments import ListArgument

class ListVariable(ExecutableVariable):
    def __init__(self):
        self.content = ListArgument({
            "default": []
        })
        self.content.getResult()
        self.total_count = 0

    @property
    def count(self):
        return len(self.content.value)

    @property
    def percentage(self):
        return self.count / self.total_count

    def append(self, item):
        self.content.value.append(item)
