from Plugins.App.Executables.Types.Extractor import Extractor

from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Types.IntArgument import IntArgument
from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

from .Number import Number
import random
import secrets

class Random(Extractor):
    class Arguments(Extractor.Arguments):
        @property
        def args(self) -> NameDictList:
            return NameDictList([
                IntArgument(
                    name = "min",
                    default = 0,
                    assertions = [
                        NotNoneAssertion()
                    ]
                ),
                IntArgument(
                    name = "max",
                    default = 100,
                    assertions = [
                        NotNoneAssertion()
                    ]
                )
            ])

    class Execute(Extractor.Execute):
        async def implementation(self, i = {}) -> None:
            num: int = random.randint(i.get('min'), i.get('max'))
            # I don't like it. I think it can be simplified? TODO
            num_rep = Number(
                call = self.outer.call
            )

            self.append(num_rep.saver.ContentUnit(
                original_name = str(num),
                content = Number.ContentUnit.ContentData(
                    number = num
                ),
                source = Number.ContentUnit.Source(
                    types = "input",
                    content = "random"
                )
            ))
