from Declarable.Arguments.Argument import Argument

class ClassArgument(Argument):
    def value(self):
        if isinstance(self.passed_value, self.get("class")):
            return self.get("class")
        else:
            return self.get("class")(self.passed_value)
