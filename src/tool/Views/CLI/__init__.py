from Executables.ExecutableCall import ExecutableCall
from Executables.list.Executables.Execute import Implementation as Execute
from Utils.Data.JSON import JSON
from App.App import App

class CLI:
    def __init__(self):
        self.app = App(context_name="cli")
        self.app.setup()

    async def call(self):
        argv = self.app.argv

        if "i" not in argv:
            self.app.logger.log("--i not passed.", section=["CLI"], kind = "error")

            return

        call = ExecutableCall(executable=Execute)
        call.passArgs(argv)

        output = await call.run_asyncely()

        if 'silent' not in argv:
            print(JSON(output.display()).dump(indent=4))
