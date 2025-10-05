from Executables.Variables.ListVariable import ListVariable
from DB.Models.Content.ContentUnit import ContentUnit

class ResultsVariable(ListVariable):
    def append(self, item: ContentUnit):
        self.content.value.append(item)
