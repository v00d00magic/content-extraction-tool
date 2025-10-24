from Objects.Outer import Outer
from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.Comparer import Comparer
from Plugins.App.Arguments.ArgumentDict import ArgumentDict

class Arguments(Outer):
    @property
    def args(self) -> NameDictList:
        return None

    @property
    def do_m_a_i(self) -> bool:
        return False

    @property
    def recursive_args(self) -> NameDictList:
        _list = NameDictList([])

        for _class in self.outer.mro:
            if hasattr(_class, 'arguments') == True:
                if hasattr(_class.arguments, 'args') == True:
                    new_arguments = _class.arguments.args
                    if new_arguments == None:
                        continue

                    for ag in new_arguments.items:
                        _list.append(ag)

        return _list

    def get(self,
            check_arguments: bool = True,
            i: ArgumentDict = None,
            raise_on_assertions: bool = True
        ) -> ArgumentDict:

        passing = None

        if check_arguments == True:
            _c = Comparer(
                compare = self.recursive_args,
                values = i,
                raise_on_assertions = raise_on_assertions,
                missing_args_inclusion = self.do_m_a_i
            )
            passing = _c.toDict()
        else:
            passing = ArgumentDict(items = i)

        return passing
