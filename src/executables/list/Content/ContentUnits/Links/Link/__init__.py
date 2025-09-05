from executables.templates.acts import Act
from declarable.Arguments import JsonArgument
from db.Models.Content.ContentUnit import ContentUnit
from db.LinkManager import LinkManager

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["pairs"] = JsonArgument({
            "scheme": {
                "items": [{
                    "link_to": "string",
                    "item_type": "string",
                    "item": "string",
                    "type": "string",
                }]
            },
            "assertion": {
                "not_null": True
            }
        })
        return params
    
    async def execute(self, i = {}):
        pairs = i.get("pairs")
        successes = 0

        for pair in pairs:
            link_to = pair.get("link_to")
            item_type = pair.get("item_type")
            item = pair.get("item")
            link_type = pair.get("type")

            item_object = ContentUnit.ids(item)
            link_manager = LinkManager(link_to)

            if link_type == "link":
                link_manager.link(item)
            else:
                link_manager.unlink(item)

            successes += 1

        return {
            "changes": successes
        }
