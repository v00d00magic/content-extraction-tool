from executables.variables.ListVariable import ListVariable
from db.Models.Content.ContentUnit import ContentUnit

class ResultsVariable(ListVariable):
    def append(self, item: ContentUnit):
        self.content.append(item)
