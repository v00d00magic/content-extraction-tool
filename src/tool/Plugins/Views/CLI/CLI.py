from colorama import init as ColoramaInit
from Plugins.Views.View import View

class CLI(View):
    class Runner(View.Runner):
        async def wrapper(self, raw_arguments):
            ColoramaInit()

            argv = self.app.argv
            if "i" not in argv:
                self.log("--i not passed.", kind = "error")
                return

            output = await self.call(raw_arguments)
            if 'silent' not in argv:
                from Plugins.Data.JSON.JSON import JSON

                print(JSON(output.display()).dump(indent=4))
