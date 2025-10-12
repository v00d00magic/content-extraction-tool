from Plugins.Data.NameDictList import NameDictList

class ApplyArgumentList(NameDictList):
    def constructor(self):
        for item in self.items:
            item.auto_apply = True
