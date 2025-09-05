from declarable.Arguments.Argument import Argument
from utils.MainUtils import parse_json

class JsonArgument(Argument):
    def value(self):
        if type(self.passed_value) == str:
            return parse_json(self.passed_value)
        else:
            return self.passed_value
