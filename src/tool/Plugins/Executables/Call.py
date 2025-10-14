from .Types.Executable import Executable
from .Types.Act import Act
from Objects.Hookable import Hookable
from Objects.Section import Section
from typing import Type

from Plugins.Arguments.Objects.ExecutableArgument import ExecutableArgument
from Plugins.Arguments.Objects.ValuesArgument import ValuesArgument
from Plugins.Arguments.Types.StringArgument import StringArgument
from Plugins.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Plugins.Data.NameDictList import NameDictList
from Plugins.Arguments.ArgumentDict import ArgumentDict
from Plugins.Executables.Response.Response import Response

from pydantic import Field
from App import app
import asyncio

class Call(Act, Hookable, Section):
    id: int = 0

    executable_class: Type[Executable] = None
    args: dict = Field(default = {})

    class Execute(Act.Execute):
        @property
        def args(self) -> NameDictList:
            return NameDictList([
                ExecutableArgument(
                    name = 'i',
                    default = None,
                    assertions = [
                        NotNoneAssertion()
                    ]
                ),
                ValuesArgument(
                    name = "execution_type",
                    default = "await",
                    values = [
                        StringArgument(
                            name = "await",
                        ),
                        StringArgument(
                            name = "thread",
                        )
                    ]
                )
            ])

        async def implementation(self, i = {}) -> Response:
            plugin_wrapper = i.get('i')
            assert plugin_wrapper != None, 'plugin not found'
            executable = plugin_wrapper.plugin()

            assert executable.meta.name != self.outer.meta.name, "can't call this (you are calling a method that calls itself)"

            response: Response = None

            match (i.get('execution_type')):
                case _:
                    response = await self.outer.execute_as_await(executable, i)

            assert response != None, "no response"

            return response

    def run_threaded(self):
        asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: asyncio.run(self.execute_as_await()) 
        )

    async def execute_as_await(self, executable, i: ArgumentDict = {}) -> Response:
        self.hooks.trigger("start")
        self.log(f"Calling {executable.meta.name} execute() with args...")

        return await executable.execute.execute(i)

    @property
    def section_name(self) -> list:
        return ["Executables", "ExecutableCall"]

    def constructor(self):
        super().constructor()
        self.id = app.executables.executable_index.getIndex()

    class HooksManager(Hookable.HooksManager):
        @property
        def events(self) -> list:
            return ["start", "progress"]

    '''
    def dump(self):
        from Plugins.Executables.Dump import Dump

        dump = Dump()
        dump.executable = self.executable_class

        _data = {}
        for key, val in self.args.items():
            _data[key] = str(val)

        dump.data = JSON(_data).dump()
        dump.save()

        self.log(f"Dumped {self.executable.getName()}, id {dump.id}", section = self.section_name)
    '''
