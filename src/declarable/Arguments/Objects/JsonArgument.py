from declarable.Arguments.Argument import Argument
from utils.Data.JSON import JSON

class JsonArgument(Argument):
    def value(self):
        if type(self.passed_value) == str:
            return JSON(self.passed_value).parse()
        else:
            return self.passed_value
