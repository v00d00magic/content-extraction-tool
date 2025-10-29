from Plugins.App.Executables.Types.Extractor import Extractor

from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Types.IntArgument import IntArgument
from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

from .Number import Number
import random
import secrets

class Random(Extractor):
    def getRandomNumber(self, min, max):
        num: int = random.randint(min, max)

        return self.setSelf(num)

    def getRandomHash(self, bytes = 32):
        _hash: str = secrets.token_urlsafe(bytes)

        return self.setSelf(_hash)

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
            num = self.outer.getRandomNumber(i.get('min'), i.get('max'))
            num_rep = Number()

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

    class Variables(Extractor.Variables):
        items = ApplyArgumentList([
            IntArgument(
                name = "number",
            )
        ])

        @property
        def common_variable(self):
            return "number"
