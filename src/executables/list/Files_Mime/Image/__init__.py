from executables.list.Files.File import Implementation as FileImplementation
from thumbnails.ImageMethod import ImageMethod

keys = {
    "image.name": {
        "en_US": "Image",
        "ru_RU": "Изображение"
    }
}

class Implementation(FileImplementation):
    docs = {
        "name": keys.get("image.name"),
    }
    inherit_from = [FileImplementation]

    @staticmethod
    async def process_item(item):
        from PIL import Image as PILImage

        new_data = {}
        common_link = item.common_link

        with PILImage.open(str(common_link.path())) as img:
            new_data = {
                "width": img.size[0],
                "height": img.size[1],
            }

        item.updateData(new_data)

        return item

    class Thumbnail(ImageMethod):
        pass
