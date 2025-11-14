from Objects.Object import Object
from Objects.Hookable import Hookable

from Plugins.App.Arguments.ArgumentDict import ArgumentDict
from Plugins.App.Executables.Response.Response import Response

from Plugins.App.Executables.Queue.RunQueue import RunQueue
from Plugins.App.Executables.Queue.RunQueueItem import RunQueueItem

from pydantic import Field
from App import app

# TODO dump
class Call(Object):
    id: int = 0
    queue: RunQueue = Field(default = None)

    async def execute_as_await(self, executable, i: ArgumentDict = {}) -> Response:
        self.hooks.trigger("start")
        self.log(f"Calling {executable.meta.name_str} execute() with args...")

        return await executable.execute.execute(i)

    async def run(self):
        return await self.queue.run()

    def constructor(self):
        super().constructor()
        self.id = app.ExecutablesTable.executable_index.getIndex()

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
