from Executables.list.Files.File import Implementation as FileImplementation
from DB.Models.Content.ContentUnit import ContentUnit
from ..Files.Image.Outer.Describe import Implementation as Describe
from ..Files.Image.Outer.ImageThumbnail import Implementation as ImageThumbnail

locale_keys = {
    "image.name": {
        "en_US": "Image",
    }
}

class Image(FileImplementation):
    @classmethod
    def getRequiredModules(cls):
        return ["pillow==11.0"]

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

    class Content(FileImplementation.Content):
        content = {
            "image": {
                "width": "int",
                "height": "int"
            }
        }
