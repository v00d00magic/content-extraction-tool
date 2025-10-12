from Objects.Outer import Outer
from Plugins.Executables.Response.Response import Response
from Plugins.Data.NameDictList import NameDictList
from Plugins.Arguments.ArgumentDict import ArgumentDict
from Plugins.Arguments.Comparer import Comparer

class Execute(Outer):
    @property
    def args(self) -> NameDictList:
        return None

    @property
    def recursive_args(self) -> NameDictList:
        _list = NameDictList([])

        for _class in self.outer.mro:
            if hasattr(_class, 'execute') == True:
                if hasattr(_class.execute, 'args') == True:
                    new_arguments = _class.execute.args
                    if new_arguments == None:
                        continue

                    for ag in new_arguments.items:
                        _list.append(ag)

        return _list

    async def implementation(self, i: ArgumentDict) -> Response:
        pass

    async def before(self, i: ArgumentDict) -> None:
        pass

    async def after(self, i: ArgumentDict) -> None:
        pass

    async def execute(self, i: dict, check_arguments: bool = True) -> Response:
        '''
        Internal method. Calls module-defined implementation() and returns what it returns
        '''

        passing = None
        if check_arguments == True:
            _c = Comparer(
                compare = self.recursive_args,
                values = i
            )
            passing = _c.toDict()
        else:
            passing = ArgumentDict(items = i)

        await self.before(passing)

        response = await self.implementation(i = passing)

        await self.after(passing)

        return response
