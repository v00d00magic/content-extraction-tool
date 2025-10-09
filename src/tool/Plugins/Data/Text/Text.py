from Plugins.Executables.Types.Representation import Representation
from Plugins.Arguments.Types.StringArgument import StringArgument
from Plugins.Arguments.ArgumentList import ArgumentList
from App import app
import re

class Text(Representation):
    class Variables(Representation.Variables):
        items = ArgumentList([
            StringArgument(
                name = "text",
                default = ""
            )
        ])

    def __init__(self, text: str):
        self.variables.items.get("text").value = text

    def getText(self):
        return self.variables.items.get("text").getValue()

    def NTFSNormalizer(self):
        safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', self.getText())
        safe_filename = re.sub(r'_+', '_', safe_filename)
        safe_filename = safe_filename.strip('_')
        if not safe_filename:
            return "unnamed"

        return safe_filename

    def cut(self, length: int = 100, multipoint: bool = True):
        newString = self.getText()[:length]

        if multipoint == False:
            return newString

        return newString + ("..." if self.data != newString else "")

    def cwdReplacement(self) -> str:
        return self.replaceCwd(str(app.src))

    def replaceCwd(self, withs: str) -> str:
        return self.getText().replace("?cwd?", withs)
