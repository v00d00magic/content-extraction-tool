from Plugins.Executables.Types.Representation import Representation
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList

from Plugins.Executables.Types.Extractor import Extractor
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
            _json = JSON()
            _json.useAsClass(data = i.get('text'))

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
        data: list | dict = None

    class Submodules(Representation.Submodules):
        items: list = [JSONFromObject, JSONFromText]

    class Variables(Representation.Variables):
        items = ApplyArgumentList([
            ObjectArgument(
                name = "json",
                default = {}
            )
        ])

    def useAsClass(self, data: dict):
        self.variables.get("json").current = data

    def getSelf(self) -> str:
        return self.variables.items.get("json").current

    def setSelf(self, new: str) -> str:
        self.variables.items.get("json").current = new

        return self.getSelf()

    def parse(self) -> dict:
        if type(self.getSelf()) == str:
            return self.setSelf(json.loads(self.getSelf()))

        return self.getSelf()

    def dump(self, indent = None) -> str:
        return json.dumps(self.getSelf(), ensure_ascii = False, indent = indent)

    def isValid(self):
        try:
            return self.getSelf() != None and type(self.getSelf()) != int and type(self.getSelf()) != str
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
