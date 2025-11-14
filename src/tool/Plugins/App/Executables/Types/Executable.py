from Objects.Object import Object
from Objects.Namespace import Namespace
from .Templates import Arguments, Execute, Saver
from typing import Any, ClassVar, Literal, List
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.Data.NameDictList import NameDictList
from pydantic import Field

class VariablesList(Object):
    items: NameDictList = None

    def constructor(self):
        self.items = NameDictList([])

    def append(self, item):
        self.items.append(item)

class EnvList(Object):
    items: NameDictList = None

    def constructor(self):
        self.items = NameDictList([])

class Executable(Object, Namespace):
    parent: Object = Field(default = None)
    call: Any = Field(default = None)

    submodule_value: ClassVar[Literal['internal', 'external']] = None
    self_name: ClassVar[str] = "None"

    meta: ClassVar[Any] = Field(default = None)
    submodules: ClassVar[Any] = Field(default = None)
    execute: Any = Field(default = None)
    saver: Any = Field(default = None)

    variables: VariablesList = None
    env_variables: EnvList = None

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

    class Saver(Saver.Saver):
        pass

    class Variables():
        items: ApplyArgumentList = ApplyArgumentList([])

    class EnvVariables():
        items: NameDictList = NameDictList([])

    @classmethod
    def use(cls, *args, **kwargs):
        return cls._callFromCode(*args, **kwargs)

    def _callFromCode(self):
        pass

    def init_subclass(cls):
        cls.arguments = cls.Arguments(cls)

    def constructor(self):
        self.variables = VariablesList()
        self.env_variables = EnvList()

        for item in self.mro:
            # TODO refactor to not use without constructor
            if hasattr(item, 'Variables'):
                for variable in self.Variables().items.toList():
                    _var = variable.__class__(name = variable.name)
                    _item = _var.copy(update=variable.dict(exclude={'current'}))
                    _item.autoApply()
                    self.variables.append(_item)

            if hasattr(item, 'EnvVariables'):
                for variable in self.EnvVariables().items.toList():
                    self.env_variables.append(variable)

        self.execute = self.Execute(self)

    @property
    def section_name(self) -> list:
        current_class = self.__class__.__mro__[0]
        name_module = current_class.__module__
        name_parts = name_module.split('.')

        return ["Executables", *name_parts]
