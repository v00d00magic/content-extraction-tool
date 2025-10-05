from Objects.Object import Object
from Plugins.App.Storage.Storage import app
import re

class Text(Object):
    def NTFSNormalizer(self, text):
        safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', text)
        safe_filename = re.sub(r'_+', '_', safe_filename)
        safe_filename = safe_filename.strip('_')
        if not safe_filename:
            return "unnamed"

        return safe_filename

    def cut(self, text, length: int = 100, multipoint: bool = True):
        newString = text[:length]

        if multipoint == False:
            return newString

        return newString + ("..." if self.data != newString else "")

    def cwdReplacement(self, text) -> str:
        return self.replaceCwd(text, str(app.src))

    def replaceCwd(self, text: str, withs: str) -> str:
        return text.replace("?cwd?", withs)
