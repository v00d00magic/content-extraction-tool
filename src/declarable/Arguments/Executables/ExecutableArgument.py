from declarable.Arguments.Argument import Argument

class ExecutableArgument(Argument):
    compare = None

    def value(self):
        from app.App import app

        return app.indexated_scripts.find(str(self.passed_value), self.compare)

    def assertion_can_be_executed(self, item):
        assert self.recieved_value.canBeExecuted() == True, "item cannot be executed"
