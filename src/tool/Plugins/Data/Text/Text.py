from Plugins.Executables.Types.Representation import Representation
from Plugins.Arguments.Types.StringArgument import StringArgument
from Plugins.Arguments.ApplyArgumentList import ApplyArgumentList
from App import app
import re

class Text(Representation):
    class Variables(Representation.Variables):
        items = ApplyArgumentList([
            StringArgument(
                name = "text",
                default = ""
            )
        ])

    class Execute(Representation.Execute):
        pass

    def useAsClass(self, text: str):
        self.variables.get("text").current = text

    def getSelf(self) -> str:
        return self.variables.items.get("text").current

    def setSelf(self, new: str) -> str:
        self.variables.items.get("text").current = new

        return self.getSelf()

    def NTFSNormalizer(self):
        safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', self.getSelf())
        safe_filename = re.sub(r'_+', '_', safe_filename)
        safe_filename = safe_filename.strip('_')
        if not safe_filename:
            safe_filename = "unnamed"

        return self.setSelf(safe_filename)

    def cut(self, length: int = 100, multipoint: bool = True) -> str:
        newString = self.getSelf()[:length]

        if multipoint == False:
            return newString

        return self.setSelf(newString + ("..." if self.data != newString else ""))

    def cwdReplacement(self) -> str:
        return self.replaceCwd(str(app.src))

    def replaceCwd(self, withs: str) -> str:
        return self.setSelf(self.getSelf().replace("?cwd?", withs))
