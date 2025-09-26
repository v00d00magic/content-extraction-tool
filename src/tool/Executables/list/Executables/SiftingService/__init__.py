from Executables.Templates.Services.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from Executables.Templates.Extractors import Extractor
from Declarable.Arguments import StringArgument, ObjectArgument

class Implementation(BaseDeclaredAtDependent):
    @classmethod
    def declare(cls):
        params = {}
        params["extractor"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["pass_args"] = ObjectArgument({
            "default": {},
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def implementation(self, i = {}):
        self.regular_extractor = Extractor.find(self.config.get('extractor'))
        self.pass_params = self.config.get('pass_args')

        await super().execute(i)
