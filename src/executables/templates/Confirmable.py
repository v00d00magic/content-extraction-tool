from typing import Dict

class Confirmable():
    '''
    Class that implies that there will be confirmation before real execute
    '''
    class PreExecute():
        args_list = []

        def __init__(self, outer):
            self.outer = outer
            self.outer_args = outer.declare_recursive()

        async def execute(self, i: dict = {}) -> Dict["list", "dict"]:
            return {
                "args": [],
                "data": {},
            }
