from Objects.Object import Object
from Objects.Namespace import Namespace
from Objects.Section import Section
from .Templates import Arguments, Meta, Execute, Saver, Variables, EnvVariables, Submodules
from typing import Any, ClassVar
from pydantic import Field

class Executable(Object, Namespace, Section):
    self_name: ClassVar[str] = "None"
    call: ClassVar[Any] = Field(default = None)
    meta: ClassVar[Any] = Field(default = None)
    submodules: ClassVar[Any] = Field(default = None)
    variables: ClassVar[Any] = Field(default = None)
    env_variables: ClassVar[Any] = Field(default = None)
    execute: Any = Field(default = None)
    saver: Any = Field(default = None)

    class Arguments(Arguments.Arguments):
        pass

    class Meta(Meta.Meta):
        pass

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

    def init_subclass(cls):
        cls.arguments = cls.Arguments(cls)
        cls.meta = cls.Meta(cls)
        cls.submodules = cls.Submodules(cls)
        cls.variables = cls.Variables(cls)
        cls.env_variables = cls.EnvVariables(cls)

    def constructor(self):
        self.execute = self.Execute(self)
        self.saver = self.Saver(self)

    def useAsClass(self) -> None:
        '''
        if you want to use this class not only in ui (view), but at code
        '''
        pass

    def getSelf(self):
        '''
        if you have used "useAtClass()" and want to get result
        '''
        return None

    def setSelf(self, new: Any):
        # code with setting self
        
        return self.getSelf()

    @property
    def section_name(self) -> list:
        _class = self.__class__.__mro__[0]
        _module = _class.__module__
        _parts = _module.split('.')

        return ["Executables", *_parts]
