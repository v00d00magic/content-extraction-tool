from Plugins.App.Executables.Queue.RunQueueItem import RunQueueItem
from Objects.Object import Object
from typing import List
from pydantic import Field

class RunQueue(Object):
    '''
    Wrapper for RunQueueItem's. It runs items from queue and provides needed arguments
    '''

    items: List[RunQueueItem] = Field(default = [])
    return_from: int = Field(default = 0)

    def append(self, item: RunQueueItem):
        self.items.append(item)
