from Objects.Object import Object
from Objects.Hookable import Hookable
from Objects.Section import Section

from Plugins.App.Arguments.ArgumentDict import ArgumentDict
from Plugins.App.Executables.Response.Response import Response

from Plugins.App.Executables.Queue.RunQueue import RunQueue

from pydantic import Field
from App import app

# TODO dump
class Call(Object, Hookable, Section):
    id: int = 0
    queue: RunQueue = None

    async def execute_as_await(self, executable, i: ArgumentDict = {}) -> Response:
        self.hooks.trigger("start")
        self.log(f"Calling {executable.meta.name_str} execute() with args...")

        return await executable.execute.execute(i)

    async def run(self):
        results_table = {}
        _i = 0

        for item in self.queue.items:
            args = item.getArguments(self.queue, results_table)

            self.log(f"Queue item {_i}: running {item} {args}")

            result = await item.run(args)
            results_table[_i] = result

            self.log(f"Queue item {_i}: got result {result}")

            _i += 1

        return results_table[self.queue.return_from]

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
        from Plugins.App.Executables.Dump import Dump

        dump = Dump()
        dump.executable = self.executable_class

        _data = {}
        for key, val in self.args.items():
            _data[key] = str(val)

        dump.data = JSON(_data).dump()
        dump.save()

        self.log(f"Dumped {self.executable.getName()}, id {dump.id}", section = self.section_name)
    '''
