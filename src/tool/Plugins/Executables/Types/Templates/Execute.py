from Objects.Outer import Outer
from Plugins.Executables.Response.Response import Response
from Plugins.Arguments.ArgumentDict import ArgumentDict
from Objects.Section import Section

class Execute(Outer, Section):
    async def implementation(self, i: ArgumentDict) -> Response:
        pass

    async def before(self, i: ArgumentDict) -> None:
        pass

    async def after(self, i: ArgumentDict) -> None:
        pass

    async def execute(self, i: dict, check_arguments: bool = True, raise_on_assertions: bool = True) -> Response:
        '''
        Internal method. Calls module-defined implementation() and returns what it returns
        '''

        passing = self.outer.arguments.get(
            check_arguments = check_arguments,
            i = i,
            raise_on_assertions = raise_on_assertions,
        )

        await self.before(passing)

        response = await self.implementation(i = passing)

        await self.after(passing)

        return response

    @property
    def section_name(self) -> list:
        return self.outer.section_name
