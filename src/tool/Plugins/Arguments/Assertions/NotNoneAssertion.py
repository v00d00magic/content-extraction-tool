from .Assertion import Assertion
from ..Argument import Argument

class NotNoneAssertion(Assertion):
    def check(self, argument: Argument):
        return argument.current != None
