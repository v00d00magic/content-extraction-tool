from pydantic import Field

from typing import Any
from Objects.Section import Section
from Objects.Object import Object
from Plugins.App.App import App

class View(Object):
    name: str = Field(default="na")
    app_wrapper: Any = None
    runner: Any = None

    # not asynco
    class AppWrapper(Section):
        section_name = ["View", "App"]

        def __init__(self, name):
            self.app = App(context_name=name)

        def run_until_complete(self, coroutine):
            self.app.loop.run_until_complete(coroutine)

    class Runner(Section):
        section_name = ["View", "Run"]

        async def wrapper(self, raw_arguments):
            pass

        async def call(self, raw_arguments):
            from Executables.list.Executables.Execute.Execute import Implementation as Execute
            from Executables.ExecutableCall import ExecutableCall

            assert "i" in raw_arguments, "i not passed"

            call = ExecutableCall(executable=Execute)
            call.passArgs(raw_arguments)

            output = await call.run_asyncely()

            return output

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),

        # Sorry but this is necessary :(

        self.app_wrapper = self.AppWrapper(self.name)
        self.setAsCommon()
        self.app_wrapper.app.consturctor()
        self.runner = self.Runner()

    def setAsCommon(self):
        from App import app

        app.setView(self)

    def loopSelf(self):
        self.app_wrapper.run_until_complete(self.runner.wrapper())
