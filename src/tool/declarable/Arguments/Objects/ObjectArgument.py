from declarable.Arguments.Argument import Argument
from utils.Data.JSON import JSON

class ObjectArgument(Argument):
    def value(self):
        if type(self.passed_value) == list:
            return self.passed_value
        elif type(self.passed_value) == str:
            return JSON(self.passed_value).parse()
        elif type(self.passed_value) == dict or type(self.passed_value) == object:
            return self.passed_value
