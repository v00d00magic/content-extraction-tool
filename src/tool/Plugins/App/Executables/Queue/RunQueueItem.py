from Objects.Object import Object
from App import app
from pydantic import Field
from typing import Literal, List

class RunQueueItemValueReplacements(Object):
    position: list = Field(default = {})
    value: str = Field(default = None)

    def set(self, change: str, to_insert: str):
        print(change)
        print(to_insert)
        return change[:self.position[0]] + str(to_insert) + change[self.position[1]:]

class RunQueueItemValue(Object):
    value: str = Field(default = None)
    replacements: List[RunQueueItemValueReplacements] = Field(default = None)

    def getValue(self, queue_link, results_table: Object):
        _val = self.value
        if self.replacements != None:
            for replace in self.replacements:
                _val = replace.set(_val, queue_link.replaceArg(replace.value, results_table))
                print(_val)

class RunQueueItem(Object):
    name: str = Field()
    arguments: dict = Field(default = {})
    db: Literal['tmp', 'instance', 'content'] = Field(default = 'tmp')

    @property
    def executable_class(self):
        return app.executables.list.find(self.name)

    def getArguments(self, queue_link, results_table: Object):
        orig_arguments = self.arguments
        returns = {}

        for key, val in orig_arguments.items():
            if type(val) != dict:
                returns[key] = val
            else:
                _obj = val
                if isinstance(val, RunQueueItemValue) == False:
                    _replacements = val.get('replacements')
                    _replaces = []
                    for item in _replacements:
                        _replaces.append(RunQueueItemValueReplacements(**item))

                    _obj = RunQueueItemValue(
                        value = val.get('value'),
                        replacements = _replaces
                    )

                returns[key] = _obj.getValue(queue_link, results_table)

        print(returns)
        return returns

    def run(self, arguments):
        assert self.executable_class != None, "executable not found"

        plugin = self.executable_class.plugin
        executable = plugin()
        executable.call = self

        # returning coroutine without await
        return executable.execute.execute(arguments)
