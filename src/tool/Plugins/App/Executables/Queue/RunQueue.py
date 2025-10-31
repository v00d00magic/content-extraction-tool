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

    @staticmethod
    def replaceArg(text, results_table_link: dict):
        # format: $0.data.text
        print(results_table_link)
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

        '''
        _iterator = 0
        for item in items:
            if item.startswith("$") == True:
                _id = int(item.replace("$", ""))
                if _iterator == 0:
                    processed_items.append(results_table_link[_id])

            _iterator += 1

        for pr_item in processed_items:
        '''

        return text
