from Objects.Object import Object
from App import app
from pydantic import Field
from typing import Literal, List
from Plugins.App.Arguments.ArgumentDict import ArgumentDict

# TODO remove spaghetti
class RunQueueItemValueReplacements(Object):
    position: list = Field(default = {})
    value: str = Field(default = None)

    def set(self, change: str, to_insert: str):
        return change[:self.position[0]] + str(to_insert) + change[self.position[1]:]

class RunQueueItemArguments():
    @staticmethod
    def getArguments(arguments: dict, results_table: Object, variables: dict) -> ArgumentDict:
        # TODO remove too many links to results and variables
        returns = ArgumentDict()

        for key, val in arguments.items():
            if type(val) != dict:
                returns.items[key] = val
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

                returns.items[key] = _obj.getValue(results_table, variables)

        return returns

    @staticmethod
    def getArgument(text, results_table_link: dict, variables: dict):
        # format: $0.data.text
        items: List[str] = text.split(".")

        def getCommonItem(item, previous_level = None, apply_modifiers: bool = True):
            if apply_modifiers == True:
                ids = None

                if item.startswith('$'):
                    ids = int(item.replace('$', ''))

                    if previous_level == None:
                        return results_table_link.get(ids)
                    else:
                        return previous_level[ids]
                elif item.startswith('#'):
                    ids = int(item.replace('#', ''))
                    variable = variables[ids]

                    return variable.current

            if type(previous_level) == dict:
                return previous_level[item]
            else:
                return getattr(previous_level, item)

        common_i = getCommonItem(items[0])
        current_level = common_i

        for item in items[1:]:
            current_level = getCommonItem(item, previous_level = current_level, apply_modifiers = True)

        return current_level

class RunQueueItemValue(Object):
    value: str = Field(default = None)
    replacements: List[RunQueueItemValueReplacements] = Field(default = None)

    def getValue(self, results_table: Object, variables: dict):
        _val = self.value
        if self.replacements != None:
            for replace in self.replacements:
                _val = replace.set(_val, RunQueueItemArguments.getArgument(replace.value, results_table, variables))

        return _val

class RunQueueItem(Object):
    name: str = Field()
    arguments: dict = Field(default = {})

    @property
    def executable_class(self):
        return app.ExecutablesTable.list.find(self.name)

class RunQueueExecuteItem(RunQueueItem):
    type: Literal['executable', 'val'] = Field(default = 'executable')
    db: Literal['tmp', 'instance', 'content'] = Field(default = 'tmp')

    def run(self, arguments: ArgumentDict, variables: dict):
        assert self.executable_class != None, f"executable with name {self.name} not found"

        plugin = self.executable_class.module
        executable = plugin()
        executable.call = self

        # returning coroutine without await
        return executable.execute.execute(arguments)
