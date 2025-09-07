from executables.templates.services.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from executables.templates.extractors import Extractor
from declarable.Arguments import StringArgument

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

    async def execute(self, i = {}):
        self.regular_extractor = Extractor.find('Rss.RSSFeed')
        self.pass_params = {
            "url": self.config.get('url'),
            'create_collection': False,
        }

        await super().execute(i)
