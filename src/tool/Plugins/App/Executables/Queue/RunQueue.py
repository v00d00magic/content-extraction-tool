from Plugins.App.Executables.Queue.RunQueueItem import RunQueueItem, RunQueueItemArguments
from .RunQueueResults import RunQueueResults
from Objects.Object import Object
from Objects.Section import Section
from typing import List
from pydantic import Field

class RunQueue(Object, Section):
    '''
    Wrapper for RunQueueItem's. It runs items from queue and provides needed arguments
    '''

    items: List[RunQueueItem] = Field(default = [])
    variables: List = Field(default = [])
    return_from: int = Field(default = 0)

    @staticmethod
    def fromJson(data: dict):
        queue = RunQueue(
            items = [],
            variables = [],
            return_from = data.get('return_from')
        )

        for item in data.get('items'):
            queue.items.append(RunQueueItem(**item))

        for variable in data.get('variables'):
            queue.variables.append(variable)

        return queue

    def append(self, item: RunQueueItem):
        self.items.append(item)

    async def run(self):
        results_table = RunQueueResults()

        for item in self.items:
            args = RunQueueItemArguments.getArguments(item.arguments, results_table)

            self.log(f"Queue item {results_table.iterator}: running {item} with {args}")

            result = await item.run(args)
            results_table.set(results_table.iterator, result)

            self.log(f"Queue item {results_table.iterator}: got results {result}")

            results_table.iterator += 1

        return results_table
