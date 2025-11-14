from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Executables.Types.Extractor import Extractor
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList

from Plugins.App.Executables.Response.Response import Response
from Plugins.App.DB.Content.ContentUnit import ContentUnit

from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.Types.StringArgument import StringArgument
from Plugins.App.Arguments.Types.IntArgument import IntArgument
from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

from App import app
import re

class Text(Representation):
    @classmethod
    def define_data(cls):
        class NewContent(Representation.ContentUnit):
            class Data(Representation.ContentUnit.Data):
                text: str

            content: Data

            def NTFSNormalizer(self):
                safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', self.content.text)
                safe_filename = re.sub(r'_+', '_', safe_filename)
                safe_filename = safe_filename.strip('_')
                if not safe_filename:
                    safe_filename = "unnamed"

                self.content.text = safe_filename

            def cut(self, length: int = 100, multipoint: bool = True) -> str:
                newString = self.content.text[:length]
                if multipoint == False:
                    return newString

                output = newString + ("..." if self.data != newString else "")

                self.content.text = output

            def replaceCwd(self) -> str:
                self.replaceCwdStrWith(str(app.src))

            def replaceCwdStrWith(self, withs: str) -> str:
                self.content.text = self.content.text.replace("?cwd?", withs)

        return NewContent

    class Submodules(Representation.Submodules):
        class ByText(Extractor):
            submodule_value = "internal"

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
                async def implementation(self, i = {}) -> None:
                    text = i.get('text')
                    name = text[0:i.get('title_cut')]
                    item = Text.ContentUnit(
                        original_name = name,
                        content = Text.ContentUnit.Data(
                            text = text
                        ),
                        source = Text.ContentUnit.Source(
                            types = "input",
                            content = "text"
                        )
                    )
                    item.flush(self.outer.call.get_db())

                    self.append(item)

    @classmethod
    def _callFromCode(cls, text: str) -> ContentUnit:
        return cls.ContentUnit(content = cls.ContentUnit.Data(text = text))
