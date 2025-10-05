from Plugins.Documentation.Documentation import Documentation
from Plugins.Arguments.Assertions import Assertions
from Objects.Object import Object
from pydantic import Field, computed_field

class Argument(Object):
    name: str = Field()
    default: any = Field(default=None)
    current: str = Field(default=None)
    is_sensitive: bool = Field(default=False)
    docs: Documentation = Field(default=None)
    assertions: Assertions = Field(default=None)

    @computed_field
    @property
    def value(self):
        return self.implementation()

    @computed_field
    @property
    def sensitive_default(self):
        return self.default

    def implementation(self):
        return self.current
