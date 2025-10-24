from .Executable import Executable
from Plugins.Executables.Response.Response import Response
from Plugins.Data.NameDictList import NameDictList
from Plugins.App.DB.Content.ContainsContentUnit import ContainsContentUnit
from Plugins.App.Arguments.Comparer import Comparer
from Plugins.App.Arguments.Objects.ValuesArgument import ValuesArgument
from Plugins.App.Arguments.Types.StringArgument import StringArgument
from typing import ClassVar

class Representation(Executable, ContainsContentUnit):
    self_name: ClassVar[str] = "Representation"

    class Arguments(Executable.Arguments):
        @property
        def args(self) -> NameDictList:
            lists = NameDictList(items = [
                ValuesArgument(
                    name = 'save',
                    default = 'tmp',
                    values = [
                        StringArgument(
                            name = 'tmp'
                        ),
                        StringArgument(
                            name = 'content'
                        ),
                        StringArgument(
                            name = 'instance'
                        )
                    ]
                )
            ])

            for item in self.outer.submodules.get(["Extractor", "Receivation"]):
                for arg in item.arguments.args.toList():
                    lists.append(arg)

            return lists

    class Execute(Executable.Execute):
        async def implementation(self, i) -> Response:
            '''
            Overrides the default Executable.Execute "implementation()" and allows for automatic extractor choosing
            You should not override this too. it's better to create single extractor
            '''

            extractors = []
            for submodule in self.outer.submodules.get(type_in=["Extractor", "Receivation"]):
                extractors.append(submodule)

            extractor = self._getSuitableExtractor(extractors, i)
            assert extractor != None, "can't find suitable extractor"

            extract = extractor()
            extract.parent = self.outer
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
