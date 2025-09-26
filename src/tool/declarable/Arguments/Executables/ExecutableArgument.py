from declarable.Arguments.Argument import Argument

class ExecutableArgument(Argument):
    compare = None

    def value(self):
        from app.App import app

        print(str(self.passed_value))
        return app.indexated_scripts.find(str(self.passed_value), self.compare)

    def assertion_not_null(self, item):
        assert self.recieved_value != None, f"not found executable with name {self.passed_value}!"
