from executables.templates.representations import Representation
from utils.ClassProperty import classproperty

class Implementation(Representation):
    @classproperty
    def required_modules(cls):
        return ["selenium", "beautifulsoup4", "fake-useragent"]

    def extractByHtml(self, i = {}):
        xml_text = i.get('html')

    def extractByUrl(self, i = {}):
        url = i.get('url')
