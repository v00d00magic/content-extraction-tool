from Declarable.Arguments.Argument import Argument

class FloatArgument(Argument):
    def implementation(self)->float:
        return float(self.passed_value)
