from Plugins.App.Executables.Queue.RunQueueItem import RunQueueItem, RunQueueItemArguments, RunQueueExecuteItem
from .RunQueueResults import RunQueueResults
from Plugins.App.Logger.LogParts.LogPrefix import LogPrefix
from Objects.Object import Object
from Objects.Section import Section
from typing import List
from pydantic import Field

class RunQueue(Object, Section):
    '''
    Wrapper for RunQueueItem's. It runs items from queue and provides needed arguments
    '''

    items: List[RunQueueItem] = Field(default = [])
    repeat: int = Field(default = 1)
    pre: List = Field(default = [])
    return_from: int | str = Field(default = 'common')

    @staticmethod
    def fromJson(data: dict):
        queue = RunQueue()

        for key, value in data.items():
            match (key):
                case 'items':
                    for item in value:
                        queue.items.append(RunQueueExecuteItem(**item))
                case 'pre':
                    for variable in value:
                        queue.pre.append(RunQueueItem(**variable))
                case _:
                    setattr(queue, key, value)

        return queue

    def parseVariables(self):
        _i = 0
        variables: dict = {}
        for var in self.pre:
            plugin = var.executable_class.module
            variables[_i] = plugin(*[], **var.arguments)

        return variables

    def append(self, item: RunQueueItem):
        self.items.append(item)

    async def run(self):
        results = RunQueueResults()
        variables = self.parseVariables()

        for repeat in range(0, self.repeat):
            for item in self.items:
                item_id = results.iterator
                prefix = LogPrefix(name = f'QueueItem|Repeat_{repeat}', id = item_id)

                self.log(f"Starting queue item #{item_id}", prefix = prefix)

                match (item.type):
                    case _:
                        args = RunQueueItemArguments.getArguments(item.arguments, results, variables)

                        result = await item.run(args, variables)
                        results.set(item_id, result)

                        self.log(f"Running executable {item} with {args}", prefix = prefix)

                self.log(f"Queue item #{item_id} has ended", prefix = prefix)

                results.iterator += 1

        return results
