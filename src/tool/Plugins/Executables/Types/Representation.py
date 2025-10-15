from .Executable import Executable
from Plugins.Executables.Response.Response import Response
from Plugins.DB.Content.ContentUnit import ContentUnit as OrigContentUnit
from Plugins.Data.NameDictList import NameDictList
from Plugins.Arguments.Comparer import Comparer
from typing import ClassVar
from pydantic import Field

class Representation(Executable):
    self_name: ClassVar[str] = "Representation"

    def init_subclass(cls):
        super().init_subclass(cls)

        class ContentUnit(OrigContentUnit):
            class Saved(OrigContentUnit.Saved):
                representation: str = Field(default = cls.meta.name)
                method: str = Field(default = cls.meta.name)

            saved: Saved = Field(default = Saved())

        cls.ContentUnit = ContentUnit

    class Arguments(Executable.Arguments):
        @property
        def args(self) -> NameDictList:
            _dict = NameDictList(items = [])

            for item in self.outer.submodules.get(["Extractor", "Receivation"]):
                for arg in item.arguments.args.toList():
                    _dict.append(arg)

            return _dict

    class Execute(Executable.Execute):
        async def implementation(self, i) -> Response:
            '''
            Overrides the default Executable.Execute "implementation()" and allows for automatic extractor choosing
            You should not override this too, it's better to create single extractor
            '''

            extractors = []
            for submodule in self.outer.submodules.get(type_in=["Extractor", "Receivation"]):
                extractors.append(submodule)

            extractor = self._getSuitableExtractor(extractors, i)
            assert extractor != None, "can't find suitable extractor"

            extract = extractor()
            self.log(f"Using extractor: {extract.meta.class_name}")

            return await extract.execute.execute(i)

        def _getSuitableExtractor(self, items: list, values: dict):
            #if len(items) == 1:
            #    return items[0]
            # ^^^ Not the best code practics

            for item in items:
                decl = Comparer(compare = item.arguments.recursive_args, values = values)

                if decl.diff():
                    return item

            return None

        def _getOptimalStrategy(self):
            pass
