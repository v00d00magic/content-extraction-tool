from Objects.Object import Object
from App import app
from pydantic import Field
from typing import Literal, List

class RunQueueItemArguments():
    @staticmethod
    def getArguments(arguments: dict, results_table: Object):
        returns = {}

        for key, val in arguments.items():
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

                returns[key] = _obj.getValue(results_table)

        return returns
    
    @staticmethod
    def getArgument(text, results_table_link: dict):
        # format: $0.data.text
        items: List[str] = text.split(".")
        common_result_link = items[0]
        common_i = int(common_result_link.replace("$", ""))
        result_in_table = results_table_link.get(int(common_i))
        current_level = result_in_table

        for item in items[1:]:
            if "$" in item:
                current_level = current_level[int(item.replace("$", ""))]
            else:
                current_level = getattr(current_level, item)

        return current_level

class RunQueueItemValueReplacements(Object):
    position: list = Field(default = {})
    value: str = Field(default = None)

    def set(self, change: str, to_insert: str):
        return change[:self.position[0]] + str(to_insert) + change[self.position[1]:]

class RunQueueItemValue(Object):
    value: str = Field(default = None)
    replacements: List[RunQueueItemValueReplacements] = Field(default = None)

    def getValue(self, results_table: Object):
        _val = self.value
        if self.replacements != None:
            for replace in self.replacements:
                _val = replace.set(_val, RunQueueItemArguments.getArgument(replace.value, results_table))

        return _val

class RunQueueItem(Object):
    name: str = Field()
    arguments: dict = Field(default = {})
    db: Literal['tmp', 'instance', 'content'] = Field(default = 'tmp')

    @property
    def executable_class(self):
        return app.executables.list.find(self.name)

    def run(self, arguments):
        assert self.executable_class != None, f"executable with name {self.name} not found"

        plugin = self.executable_class.plugin
        executable = plugin()
        executable.call = self

        # returning coroutine without await
        return executable.execute.execute(arguments)
