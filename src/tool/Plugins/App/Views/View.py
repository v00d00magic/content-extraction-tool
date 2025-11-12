from pydantic import Field, computed_field

from typing import Any, ClassVar, List
from Objects.Configurable import Configurable
from Objects.Section import Section
from Objects.Object import Object
from Plugins.App.App import App
from Objects.ClassProperty import classproperty

class View(Object, Configurable):
    '''
    "App" wrapper. Contains methods and subclasses for simplier executables calling and initialization
    '''

    app: Any = None
    caller: Any = None
    wrapper: Any = None

    class CommonApp(Section):
        '''
        Wrapper of the app. The __init__ function initializes it and gives view's name.
        Sadly but it doesn't use pydantic :(
        '''

        def __init__(self, outer):
            self.outer = outer
            self.app = App()
            self.app.context_name = outer.class_name

        def loop_with_argv(self):
            self.loop(self.app.argv)

        def loop(self, argv):
            '''
            Uses the "caller" as the common asyncio loop
            '''

            self.app.loop.run_until_complete(self.outer.wrapper.call(argv))

    class Caller(Section):
        '''
        Thing that uses Plugins.App.Executables.Call
        '''
        def __init__(self, outer):
            self.outer = outer

        @property
        def section_name(self) -> list:
            return ["View", "Runner"]

    class Wrapper(Section):
        '''
        View's peculiarities. Currently there is two definable functions: call and constructor
        '''
        def __init__(self, outer):
            self.outer = outer
            self.constructor()

        async def call(self, argv: dict = {}):
            pass

        async def _call(self, queue: List):
            from Plugins.App.Executables.Call import Call

            call = Call(queue = queue)
            output = await call.run()

            return output

        def constructor(self):
            pass

    def initializeApp(self):
        self.app = self.CommonApp(self)
        self.app.app._constructor()
        self.app.app.loadPlugins()

    def initializeCaller(self):
        self.caller = self.Caller(self)

    def initializeWrapper(self):
        self.wrapper = self.Wrapper(self)

    def constructor(self):
        '''
        Initalizing everything together. I don't like this code part tbh
        '''
        self.setAsCommon()
        self.initializeApp()
        self.initializeCaller()
        self.initializeWrapper()

        self.app.app.Logger.log(f"Loaded view {self.class_name}")

    def setAsCommon(self):
        '''
        Sets link that can be used as

        from App import app

        app.Logger.log(...)
        '''
        from App import app

        app.setView(self)
