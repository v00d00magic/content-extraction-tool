from Plugins.App.Documentation.Documentation import Documentation
from .Assertions.Assertion import Assertion
from Objects.Object import Object
from typing import Any, List
from pydantic import Field, computed_field

class Argument(Object):
    name: str = Field()
    default: Any = Field(default=None)
    input_value: str = Field(default=None) # can't find name for this but its about an input value (!). I think it is a string in the most cases
    is_sensitive: bool = Field(default=False)
    docs: Documentation = Field(default=None)
    assertions: List[Assertion] = Field(default=[])

    auto_apply: bool = Field(default=False)
    current: Any = Field(default=None)

    # This is an abstract method.
    # I think it should pass self.inputs in i ? i={} as settings will not be used anyway
    def implementation(self, i = {}) -> Any:
        return self.value

    def getValue(self, i = {}) -> Any:
        return self.implementation(i)

    def setInput(self, value):
        self.input_value = value

    @computed_field
    @property
    def inputs(self) -> Any:
        if self.input_value == None:
            return self.default

        return self.input_value

    @computed_field
    @property
    def sensitive_default(self) -> Any:
        return self.default

    def checkAssertions(self):
        for assertion in self.assertions:
            assertion.check(self)

    def constructor(self):
        if self.auto_apply == True:
            self.autoApply()

    def autoApply(self):
        self.current = self.getValue()
