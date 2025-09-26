from Executables.Templates.services.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from Executables.Templates.extractors import Extractor
from Declarable.Arguments import StringArgument

class Implementation(BaseDeclaredAtDependent):
    @classmethod
    def declare(cls):
        params = {}
        params["url"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def implementation(self, i = {}):
        self.regular_extractor = Extractor.find('Rss.RSSFeed')
        self.pass_params = {
            "url": self.config.get('url'),
            'create_collection': False,
        }

        await super().execute(i)
