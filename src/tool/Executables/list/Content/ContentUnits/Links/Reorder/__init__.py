from Executables.Templates.Acts import Act
from Declarable.Arguments import IntArgument
from DB.Models.Content.ContentUnit import ContentUnit
from DB.Links.LinkManager import LinkManager

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["item_1"] = IntArgument({})
        params["item_2"] = IntArgument({})
        return params
    
    async def implementation(self, i = {}):
        item_1 = i.get("item_1")
        item_2 = i.get("item_2")

        return {
            "changes": 1
        }
