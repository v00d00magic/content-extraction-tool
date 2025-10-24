from pydantic import Field

from typing import Any
from Objects.Section import Section
from Objects.Object import Object
from Plugins.App.App import App

class View(Object):
    name: str = Field(default="View")
    app_wrapper: Any = None
    runner: Any = None

    # not asynco
    class AppWrapper(Section):
        @property
        def section_name(self) -> list:
            return ["View", "App"]

        def __init__(self, name):
            self.app = App()
            self.app.context_name = name

        def run_until_complete(self, coroutine):
            self.app.loop.run_until_complete(coroutine)

    class Runner(Section):
        @property
        def section_name(self) -> list:
            return ["View", "Run"]

        def __init__(self, outer):
            self.outer = outer

        async def wrapper(self, raw_arguments):
            pass

        async def call(self, raw_arguments):
            from Plugins.Executables.Call import Call

            call = Call()
            output = await call.execute.execute(raw_arguments)

            return output

    def constructor(self):
        # Sorry but this is necessary :(

        self.app_wrapper = self.AppWrapper(self.name)
        self.setAsCommon()
        self.app_wrapper.app.consturctor()
        self.runner = self.Runner(self)
        self.app_wrapper.app.Logger.log("Loaded view")

    def setAsCommon(self):
        from App import app

        app.setView(self)

    def loopSelfAndRunExecute(self):
        self.app_wrapper.run_until_complete(self.runner.wrapper(self.app_wrapper.app.argv))
