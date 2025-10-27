from pydantic import Field

from typing import Any, ClassVar
from Objects.Configurable import Configurable
from Objects.Section import Section
from Objects.Object import Object
from Plugins.App.App import App

class View(Object, Configurable):
    name: ClassVar[str] = "None"
    app_wrapper: Any = None
    runner: Any = None
    subclass: Any = None

    # not asynco
    class AppWrapper(Section):
        def __init__(self, name):
            self.app = App()
            self.app.context_name = name

        def run_until_complete(self, coroutine):
            self.app.loop.run_until_complete(coroutine)

    class Runner(Section):
        def __init__(self, outer):
            self.outer = outer

        async def wrapper(self, raw_arguments):
            pass

        async def call(self, raw_arguments):
            from Plugins.Executables.Call import Call

            call = Call()
            output = await call.execute.execute(raw_arguments)

            return output

    class Subclass(Section):
        def __init__(self, outer):
            self.outer = outer
            self.constructor()

        def constructor(self):
            pass

    def constructor(self):
        # Sorry but this is necessary :(

        self.app_wrapper = self.AppWrapper(self.name)
        self.setAsCommon()
        self.app_wrapper.app._constructor()
        self.runner = self.Runner(self)
        self.subclass = self.Subclass(self)
        self.app_wrapper.app.Logger.log(f"Loaded view {self.name}")

    def setAsCommon(self):
        from App import app

        app.setView(self)

    def loopSelfAndRunExecute(self):
        self.app_wrapper.run_until_complete(self.runner.wrapper(self.app_wrapper.app.argv))
