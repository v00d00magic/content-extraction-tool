from ...Arguments.Argument import Argument
from typing import List
from pydantic import Field, computed_field
from App import app

# its like <select> in html or radioboxes idk
class ValuesArgument(Argument):
    values: List[Argument] = Field(default = [])

    def implementation(self, i = {}):
        is_in = False

        for value in self.values:
            if self.inputs == value.name:
                is_in = True

        assert is_in == True, "not allowed value"

        return self.inputs
