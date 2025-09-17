from db.Models.Content.ThumbnailUnit import ThumbnailUnit
from executables.templates.Executable import Executable
from app.App import logger

class Outer(Executable):
    # must not return anything
    def __init__(self, original):
        self.original = original

    @classmethod
    def ThumbnailUnit(cls):
        logger.log("Created new ThumbnailUnit", section="Saveable")

        return ThumbnailUnit()
