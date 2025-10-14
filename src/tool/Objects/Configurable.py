from Plugins.Data.NameDictList import NameDictList
from Objects.ClassProperty import classproperty
from App import app

class Configurable:
    @classproperty
    def options(cls) -> NameDictList:
        pass

    @classmethod
    def update(cls):
        options = cls.options
        if options == None:
            return

        for name, item in options.toDict().items():
            app.settings[name] = item

    def init_subclass(cls):
        cls.update()
