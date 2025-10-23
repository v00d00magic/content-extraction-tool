from Plugins.Executables.Types.Executable import Executable
from Plugins.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.Executables.Response.ModelsResponse import ModelsResponse
from Plugins.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.DB.Content.ContentUnit import ContentUnit

from typing import ClassVar

class Extractor(Executable):
    self_name: ClassVar[str] = "Extractor"

    class Variables(Executable.Variables):
        from Plugins.Arguments.Objects.ListArgument import ListArgument

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

            return ModelsResponse(data = self.outer.variables.get("items").current)
