from utils.ClassProperty import classproperty
from importlib.metadata import distributions

class Runnable:
    base_categories = ["template", "base"]
    available = ['web', 'cli']
    _default_sub = True

    @classproperty
    def required_modules(cls):
        return []

    # Comparisons

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

        for required_module in cls.required_modules:
            if required_module in all_installed:
                satisf_libs.append(required_module)

        return len(satisf_libs) == len(cls.required_modules)

    @classproperty
    def main_module(cls):
        if hasattr(cls, "outer") == False:
            return None

        for item in cls.__mro__:
            if getattr(item, "outer", None) != None:
                return item.outer

    @classmethod
    def full_name(cls):
        _parts = cls.__module__.split('.')
        if _parts[-1] == _parts[-2]:
            return ".".join(_parts[2:-1])

        return ".".join(_parts[2:])

    async def execute(self, i):
        if hasattr(self, "beforeExecute") == True:
            self.beforeExecute(i)

        return await self.implementation(i)
