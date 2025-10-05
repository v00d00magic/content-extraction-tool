from Objects.classproperty import classproperty
from importlib.metadata import distributions

class Runnable:
    @classmethod
    def doDefaultAppending(cls):
        return True

    @classmethod
    def getAvailableAt(cls):
        return ['web', 'cli']

    @classmethod
    def getRequiredModules(cls):
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

    @classmethod
    def getName(cls):
        '''
        Splitting full module path and joining it by dot
        '''

        _parts = cls.__module__.split('.')
        if _parts[-1] == _parts[-2]:
            return ".".join(_parts[2:-1])

        return ".".join(_parts[2:])

    async def execute(self, i):
        '''
        Internal method. Returns result and calls module-defined implementation()
        '''

        if hasattr(self, "beforeExecute") == True:
            self.beforeExecute(i)

        response = await self.implementation(i)
        if response == None:
            return self.getResult()

        return response
