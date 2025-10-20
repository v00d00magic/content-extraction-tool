from Plugins.Executables.Types.Representation import Representation
from Plugins.Executables.Types.Extractor import Extractor
from Plugins.Arguments.ApplyArgumentList import ApplyArgumentList

from Plugins.Executables.Response.Response import Response
from Plugins.Executables.Response.ModelsResponse import ModelsResponse
from Plugins.DB.Content.ContentUnit import ContentUnit

from Plugins.Data.NameDictList import NameDictList
from Plugins.Arguments.Types.StringArgument import StringArgument
from Plugins.Arguments.Types.IntArgument import IntArgument
from Plugins.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

from App import app
import re

class TextExtractor(Extractor):
    class Arguments(Extractor.Arguments):
        @property
        def args(self) -> NameDictList:
            return NameDictList([
                StringArgument(
                    name = "text",
                    assertions = [
                        NotNoneAssertion()
                    ]
                ),
                IntArgument(
                    name = "title_cut",
                    default = 100
                )
            ])

    class Execute(Extractor.Execute):
        async def implementation(self, i = {}) -> ModelsResponse:
            text = i.get('text')
            name = text[0:i.get('title_cut')]
            res = Text.ContentUnit(
                original_name = name,
                content = Text.ContentUnit.ContentData(
                    text = text
                ),
                source = Text.ContentUnit.Source(
                    types = "input",
                    content = "text"
                )
            )
            res.flush()

            return ModelsResponse(data = [res])

class Text(Representation):
    class ContentUnit(Representation.ContentUnit):
        class ContentData(Representation.ContentUnit.ContentData):
            text: str

        content: ContentData

    class Submodules(Representation.Submodules):
        items: list = [TextExtractor]

    class Variables(Representation.Variables):
        items = ApplyArgumentList([
            StringArgument(
                name = "text",
                default = ""
            )
        ])

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
