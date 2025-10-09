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

                print(JSON(output.display()).dump(indent=4))
