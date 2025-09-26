from Declarable.Arguments.Argument import Argument

class IntArgument(Argument):
    def value(self)->int:
        return int(self.passed_value)
