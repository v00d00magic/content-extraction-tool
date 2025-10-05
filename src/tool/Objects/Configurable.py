from Plugins.Arguments.ArgumentList import ArgumentList
from App import app

class Configurable:
    @property
    def options() -> ArgumentList:
        pass

    @classmethod
    def update(cls):
        app.options.update(cls.options.toDict())

    def __init_subclass__(cls):
        cls.update()
