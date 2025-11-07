from Plugins.App.Executables.Queue.RunQueue import RunQueue
from Plugins.App.Executables.Queue.RunQueueItem import RunQueueItem
from colorama import init as ColoramaInit
from ..View import View

class CLI(View):
    class Wrapper(View.Wrapper):
        async def call(self, argv: dict = {}):
            from Plugins.Data.JSON import JSON

            ColoramaInit()

            print(argv)
            common_input = argv.get('i')
            common_args = argv.copy()
            common_args.pop('i')
            is_silent = argv.get('silent') == "1"

            if common_input == None:
                # I think we should raise there?
                self.log("--i not passed.", kind = "error")
                return

            queue = RunQueue()
            # TODO change this check
            if common_input[0] in ["[", "{"]:
                _json = JSON.use(data = common_input)
                _json.parse()

                queue_items = _json.content.data
                queue = RunQueue.fromJson(queue_items)
            else:
                queue.append(RunQueueItem(
                    name = common_input,
                    arguments = common_args,
                    db = "content"
                ))

            output = await self._call(queue)
            if is_silent == False:
                _json = JSON.use(data = output.getResults(queue.return_from).toDict())

                print(_json.dump(indent=4))
