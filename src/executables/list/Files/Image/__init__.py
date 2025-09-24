from executables.list.Files.File import Implementation as FileImplementation
from db.Models.Content.ContentUnit import ContentUnit
from .Outer.Describe import Implementation as Describe
from .Outer.ImageThumbnail import Implementation as ImageThumbnail

locale_keys = {
    "image.name": {
        "en_US": "Image",
    }
}

class Implementation(FileImplementation):
    @classmethod
    def getInheritFrom(cls):
        return [FileImplementation]

    @classmethod
    def outerList(cls):
        return [Describe, ImageThumbnail]

    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("image.name"),
        }
