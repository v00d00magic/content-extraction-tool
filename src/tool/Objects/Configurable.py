from Objects.ClassProperty import classproperty
from App import app

class Configurable:
    @classproperty
    def options(cls): #  -> NameDictList
        pass

    @classmethod
    def applyToGlobalSettings(cls):
        options = cls.options
        if options == None:
            return

        for name, item in options.toDict().items():
            app.settings[name] = item

    def init_subclass(cls):
        cls.applyToGlobalSettings()
