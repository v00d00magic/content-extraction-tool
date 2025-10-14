from colorama import init as ColoramaInit
from Plugins.Views.View import View

class CLI(View):
    class Runner(View.Runner):
        async def wrapper(self, raw_arguments):
            ColoramaInit()

            if "i" not in raw_arguments:
                self.log("--i not passed.", kind = "error")
                return

            output = await self.call(raw_arguments)
            if 'silent' not in raw_arguments:
                from Plugins.Data.JSON.JSON import JSON

                _json = JSON()
                _json.useAsClass(data = output.toDict())

                print(_json.dump(indent=4))
