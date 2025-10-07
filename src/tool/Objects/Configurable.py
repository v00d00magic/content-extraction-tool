from Plugins.Arguments.ArgumentList import ArgumentList
from Objects.classproperty import classproperty
from App import app

class Configurable:
    @classproperty
    def options(cls) -> ArgumentList:
        pass

    @classmethod
    def update(cls):
        for name, item in cls.options.toDict().items():
            app.settings[name] = item

    def __init_subclass__(cls):
        cls.update()
