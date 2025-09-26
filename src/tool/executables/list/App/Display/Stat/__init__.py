from executables.templates.acts import Act
from db.Models.Content.ContentUnit import ContentUnit

class Implementation(Act):
    async def implementation(self, i = {}):
        content_units = ContentUnit.select()

        return {
            "content_units": {
                "total_count": content_units.count()
            }
        }
