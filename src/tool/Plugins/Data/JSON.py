from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.App.Arguments.Types.StringArgument import StringArgument

from Plugins.App.Executables.Types.Extractor import Extractor
from Plugins.Data.NameDictList import NameDictList
from Plugins.App.DB.Content.ContentUnit import ContentUnit
# from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

import json

class JSON(Representation):
    @classmethod
    def define_data(cls):
        class NewContent(Representation.ContentUnit):
            class Data(Representation.ContentUnit.Data):
                data: list | dict | str

            content: Data

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

        return NewContent

    class Submodules(Representation.Submodules):        
        class ByObject(Extractor):
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
                    item = JSON.ContentUnit(
                        original_name = 'JSON',
                        content = JSON.ContentUnit.Data(
                            data = i.get('object')
                        ),
                        source = JSON.ContentUnit.Source(
                            types = "input",
                            content = "object"
                        )
                    )
                    item.flush(self.outer.call.get_db())

                    self.append(item)

        class ByText(Extractor):
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
                        original_name = 'JSON',
                        content = JSON.ContentUnit.Data(
                            data = _json.parse()
                        ),
                        source = JSON.ContentUnit.Source(
                            types = "input",
                            content = "text"
                        )
                    ))

    @classmethod
    def _callFromCode(cls, data: list | dict) -> ContentUnit:
        return cls.ContentUnit(content = cls.ContentUnit.Data(data = data))
