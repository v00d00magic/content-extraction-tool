from Plugins.Arguments.ArgumentList import ArgumentList
from Objects.classproperty import classproperty
from App import app

class Configurable:
    @classproperty
    def options(cls) -> ArgumentList:
        pass

    @classmethod
    def update(cls):
        app.settings.update(cls.options.toDict())

    def __init_subclass__(cls):
        cls.update()
