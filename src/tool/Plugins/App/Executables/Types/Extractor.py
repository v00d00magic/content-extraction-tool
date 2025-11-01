from Plugins.App.Executables.Types.Executable import Executable
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Executables.Response.ModelsResponse import ModelsResponse
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.App.DB.Content.ContentUnit import ContentUnit

from typing import ClassVar

class Extractor(Executable):
    self_name: ClassVar[str] = "Extractor"

    class Variables(Executable.Variables):
        from Plugins.App.Arguments.Objects.ListArgument import ListArgument

        items = ApplyArgumentList([
            ListArgument(
                name = 'items',
                orig = ObjectArgument(
                    name = 'item',
                    object = ContentUnit
                ),
                default = []
            )
        ])

    class Execute(Executable.Execute):
        def append(self, out: ContentUnit):
            self.outer.variables.items.get("items").append(out)

        async def implementation(self, i = {}) -> None:
            pass

        async def implementation_wrap(self, i = {}) -> ModelsResponse:
            await self.implementation(i)

            print("ITEMS@@@@@@@@@", self.outer.variables.get("items"))
            return ModelsResponse(data = self.outer.variables.get("items").current)
