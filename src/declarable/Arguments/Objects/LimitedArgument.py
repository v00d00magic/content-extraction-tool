from declarable.Arguments.Argument import Argument
from utils.Data.JSON import JSON

class LimitedArgument(Argument):
    def value(self):
        inp = str(self.passed_value)
        if len(inp) == 0:
            if self.data.get('return_none_on_empty', True) == True:
                return self.default()

        return inp

    def special_assertions(self, inp):
        __allowed = self.data.get("values")

        assert inp in __allowed, f"not valid value, {self.data.get('name')}={self.passed_value} (available: {JSON(self.data.get('values')).dump()})"
