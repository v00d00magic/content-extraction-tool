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
        return app.executables.list.find(self.name).plugin

    def run(self):
        executable = self.executable_class()
        executable.call = self

        # returning coroutine without await
        return executable.execute.execute(self.arguments)
