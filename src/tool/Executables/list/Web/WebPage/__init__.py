from Executables.Templates.Representations import Representation
from Utils.ClassProperty import classproperty

class Implementation(Representation):
    @classproperty
    def getRequiredModules(cls):
        return ["selenium", "beautifulsoup4", "fake-useragent"]

    def extractByHtml(self, i = {}):
        xml_text = i.get('html')

    def extractByUrl(self, i = {}):
        url = i.get('url')
