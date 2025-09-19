from utils.Data.List import List
from utils.Wrap import Wrap

class LogSection(Wrap):
    SECTION_ACTS = 'Acts'
    SECTION_DB = 'DB'
    SECTION_EXECUTABLES = 'Executables'
    SECTION_EXTRACTORS = 'Extractors'
    SECTION_LINKAGE = 'Linkage'
    SECTION_SERVICES = 'Services'
    SECTION_SAVEABLE = 'Saveable'
    SECTION_WEB = 'Web'

    section: list

    def __init__(self, data):
        super().__init__(data)

        if type(data.get("section")) == list:
            self.section = data.get("section")
        else:
            self.section = data.get("section").split("!")

    def str(self):
        return "!".join(self.section)
