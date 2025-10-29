from Objects.Object import Object
from App import app
from pydantic import Field
from typing import Literal

class RunQueueItem(Object):
    name: str = Field()
    arguments: dict = Field(default = {})
    db: Literal['tmp', 'instance', 'content'] = Field(default = 'tmp')

    @property
    def executable_class(self):
        return app.executables.list.find(self.name)

    def getReplacedArguments(self, results_table: Object):
        return self.arguments

    def run(self, arguments):
        assert self.executable_class != None, "executable not found"

        plugin = self.executable_class.plugin
        executable = plugin()
        executable.call = self

        # returning coroutine without await
        return executable.execute.execute(arguments)
