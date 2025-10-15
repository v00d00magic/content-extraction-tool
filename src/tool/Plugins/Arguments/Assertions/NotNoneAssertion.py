from .Assertion import Assertion
from ..Argument import Argument

class NotNoneAssertion(Assertion):
    def check(self, argument: Argument):
        assert argument.current != None, f"{argument.name} not passed"
