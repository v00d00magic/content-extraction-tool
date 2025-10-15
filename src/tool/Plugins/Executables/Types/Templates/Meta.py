from Objects.Outer import Outer
from Objects.ClassProperty import classproperty
from importlib.metadata import distributions

class Meta(Outer):
    @classmethod
    def getAvailableAt(cls):
        return ['web', 'cli', '*']

    @classmethod
    def getRequiredModules(cls):
        return []

    @classmethod
    def doDefaultAppending(cls):
        return True

    @classmethod
    def isAbstract(cls):
        return False
        # FIXME rewrite
        return cls.category.lower() in cls.base_categories

    @classmethod
    def isHidden(cls):
        return getattr(cls, "hidden", False) == True

    @classmethod
    def canBeExecuted(cls):
        return cls.isAbstract() == False and cls.isHidden() == False

    @classmethod
    def canBeUsedAt(cls, at):
        return at in cls.available

    @classmethod
    def isModulesInstalled(cls):
        all_installed = {dist.metadata["Name"].lower() for dist in distributions()}
        satisf_libs = []

        for required_module in cls.getRequiredModules():
            module_versions = required_module.split("==")
            module_name = module_versions[0]

            if module_name in all_installed:
                satisf_libs.append(module_name)

        print(satisf_libs)
        return len(satisf_libs) == len(cls.getRequiredModules())

    @classproperty
    def main_module(cls):
        if hasattr(cls, "outer") == False:
            return None

        for item in cls.__mro__:
            if getattr(item, "outer", None) != None:
                return item.outer

    @property
    def name(self):
        _class = self.outer.__mro__[0]
        _module = _class.__module__
        _parts = _module.split('.')
        _parts = _parts[1:] # cut off "Plugins."

        return ".".join(_parts)

    @property
    def class_name(self):
        return self.name + "." + self.outer.__name__
