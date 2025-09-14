from executables.list.Files.File import Implementation as FileImplementation
from db.Models.Content.ContentUnit import ContentUnit

keys = {
    "image.name": {
        "en_US": "Image",
        "ru_RU": "Изображение"
    }
}

class Implementation(FileImplementation):
    inherit_from = [FileImplementation]

    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("image.name"),
        }

    @staticmethod
    async def process_item(item: ContentUnit):
        from PIL import Image as PILImage

        new_data = {}
        common_link = item.common_link

        with PILImage.open(str(common_link.path())) as img:
            item.Outer.update({
                "width": img.size[0],
                "height": img.size[1],
            })

        return item
