from pydantic import BaseModel, computed_field
from Objects.Outer import Outer
from importlib.metadata import distributions
from .ClassProperty import classproperty

class Object(BaseModel):
    # we can't use __init__ because of fields initialization, so we creating second constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.constructor(self)

    # do not copy *args and **kwargs, ok?
    def constructor(self):
        pass

    def toJson(self):
        return self.model_dump(mode='json')

    @classproperty
    def mro(cls) -> list:
        return cls.__mro__

    @classproperty
    def class_module(cls) -> str:
        return cls.__module__

    @classproperty
    def class_name(cls) -> list:
        return cls.__name__

    def init_subclass(cls):
        cls.meta = cls.Meta(cls)

    def __init_subclass__(cls):
        for item in cls.mro:
            if hasattr(item, "init_subclass") == True:
                getattr(item, "init_subclass")(cls)

            if item.__name__ == "BaseModel":
                item.__init_subclass__()

    class Meta(Outer):
        @classmethod
        def getAvailableAt(cls):
            return ['web', 'cli', '*']

        @classmethod
        def getRequiredModules(cls):
            return []

        @classmethod
        def isAbstract(cls):
            return False
            # FIXME rewrite
            return cls.category.lower() in cls.base_categories

        @classmethod
        def isHidden(cls):
            return getattr(cls, "hidden", False) == True

        @classmethod
        def isModulesInstalled(cls):
            all_installed = {dist.metadata["Name"].lower() for dist in distributions()}
            satisf_libs = []

            for required_module in cls.getRequiredModules():
                module_versions = required_module.split("==")
                module_name = module_versions[0]

                if module_name in all_installed:
                    satisf_libs.append(module_name)

            return len(satisf_libs) == len(cls.getRequiredModules())

        @classproperty
        def main_module(cls):
            if hasattr(cls, "outer") == False:
                return None

            for item in cls.__mro__:
                if getattr(item, "outer", None) != None:
                    return item.outer

        @property
        def name_str(self):
            return ".".join(self.name)

        @property
        def name(self):
            _class = self.outer.__mro__[0]
            _module = _class.__module__
            _parts = _module.split('.')
            _parts = _parts[1:] # cut off "Plugins."

            return _parts

        @property
        def class_name(self):
            return self.name + [self.outer.__name__]

        @property
        def class_name_str(self):
            return ".".join(self.class_name)
