from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList

from Plugins.App.Executables.Types.Extractor import Extractor
from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.Types.StringArgument import StringArgument
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
# from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

import json

class JSONFromObject(Extractor):
    class Arguments(Extractor.Arguments):
        @property
        def args(self) -> NameDictList:
            return NameDictList([
                ObjectArgument(
                    name = "object"
                )
            ])

    class Execute(Extractor.Execute):
        async def implementation(self, i = {}) -> None:
            self.append(self.outer.parent.saver.ContentUnit(
                original_name = 'json data',
                content = JSON.ContentUnit.ContentData(
                    data = i.get('object')
                ),
                source = JSON.ContentUnit.Source(
                    types = "input",
                    content = "object"
                )
            ))

class JSONFromText(Extractor):
    class Arguments(Extractor.Arguments):
        @property
        def args(self) -> NameDictList:
            return NameDictList([
                StringArgument(
                    name = "text"
                )
            ])

    class Execute(Extractor.Execute):
        async def implementation(self, i = {}) -> None:
            _json = JSON(data = i.get('text'))

            self.append(self.outer.parent.saver.ContentUnit(
                original_name = 'json data',
                content = JSON.ContentUnit.ContentData(
                    data = _json.parse()
                ),
                source = JSON.ContentUnit.Source(
                    types = "input",
                    content = "text"
                )
            ))

class JSON(Representation):
    class ContentUnit(Representation.ContentUnit):
        class ContentData(Representation.ContentUnit.ContentData):
            data: list | dict | str

        content: ContentData

        def parse(self) -> dict:
            if type(self.content.data) == str:
                self.content.data = json.loads(self.content.data)

        def dump(self, indent = None) -> str:
            return json.dumps(self.content.data, ensure_ascii = False, indent = indent)

        def isValid(self):
            try:
                return self.content.data != None and type(self.content.data) != int and type(self.content.data) != str
            except json.JSONDecodeError:
                return False
            except TypeError:
                return False

    class Submodules(Representation.Submodules):
        items: list = [JSONFromObject, JSONFromText]

    class Variables(Representation.Variables):
        items = ApplyArgumentList([
            ObjectArgument(
                name = "json",
                default = {}
            )
        ])

        @property
        def common_variable(self):
            return "json"

    @classmethod
    def _callFromCode(cls, data: list | dict) -> ContentUnit:
        return cls.ContentUnit(content = cls.ContentUnit.ContentData(data = data))
