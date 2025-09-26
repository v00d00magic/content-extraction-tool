from Utils.Data.List import List
from Utils.Wrap import Wrap

class LogSection(Wrap):
    section: list

    def __init__(self, data):
        super().__init__(data)

        if type(data.get("section")) == list:
            self.section = data.get("section")
        else:
            self.section = data.get("section").split("!")

    def str(self):
        return "!".join(self.section)
