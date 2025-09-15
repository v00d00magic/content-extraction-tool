from executables.list.Files.File import Implementation as FileImplementation
from db.Models.Content.ContentUnit import ContentUnit
from .Outer.Image import Implementation as Image
from .Outer.ImageThumbnail import Implementation as ImageThumbnail

locale_keys = {
    "image.name": {
        "en_US": "Image",
        "ru_RU": "Изображение"
    }
}

class Implementation(FileImplementation):
    @classmethod
    def inherit_from(cls):
        return [FileImplementation]

    @classmethod
    def outer_list(cls):
        return [Image, ImageThumbnail]

    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("image.name"),
        }
