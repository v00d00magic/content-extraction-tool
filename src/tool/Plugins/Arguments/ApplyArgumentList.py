from Plugins.Data.NameDictList import NameDictList

class ApplyArgumentList(NameDictList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for item in self.items:
            item.auto_apply = True
            item.autoApply()
