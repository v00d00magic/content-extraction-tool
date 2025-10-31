from Objects.Object import Object
from Objects.Namespace import Namespace
from Objects.Section import Section
from .Templates import Arguments, Execute, Saver, Variables, EnvVariables, Submodules
from typing import Any, ClassVar, Literal
from pydantic import Field

class Executable(Object, Namespace, Section):
    parent: Object = Field(default = None)
    call: Any = Field(default = None)

    submodule_value: ClassVar[Literal['internal', 'external']] = None
    self_name: ClassVar[str] = "None"

    meta: ClassVar[Any] = Field(default = None)
    submodules: ClassVar[Any] = Field(default = None)
    variables: ClassVar[Any] = Field(default = None)
    env_variables: ClassVar[Any] = Field(default = None)
    execute: Any = Field(default = None)
    saver: Any = Field(default = None)

    class Arguments(Arguments.Arguments):
        pass

    class Meta(Object.Meta):
        @classmethod
        def doDefaultAppending(cls):
            return True

        @classmethod
        def canBeExecuted(cls):
            return cls.isAbstract() == False and cls.isHidden() == False

        @classmethod
        def canBeUsedAt(cls, at):
            return at in cls.available

    class Execute(Execute.Execute):
        pass

    class Submodules(Submodules.Submodules):
        pass

    class Saver(Saver.Saver):
        pass

    class Variables(Variables.Variables):
        pass

    class EnvVariables(EnvVariables.EnvVariables):
        pass

    @classmethod
    def use(cls, *args, **kwargs):
        return cls._callFromCode(*args, **kwargs)

    def _callFromCode(self):
        pass

    def init_subclass(cls):
        cls.arguments = cls.Arguments(cls)
        cls.submodules = cls.Submodules(cls)
        cls.variables = cls.Variables(cls)
        cls.env_variables = cls.EnvVariables(cls)

    def constructor(self):
        self.execute = self.Execute(self)
        self.saver = self.Saver(self)

    @property
    def section_name(self) -> list:
        current_class = self.__class__.__mro__[0]
        name_module = current_class.__module__
        name_parts = name_module.split('.')

        return ["Executables", *name_parts]
