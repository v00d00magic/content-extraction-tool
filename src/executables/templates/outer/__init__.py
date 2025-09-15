from db.Models.Content.ThumbnailUnit import ThumbnailUnit
from executables.templates.Executable import Executable
from app.App import logger

class Outer(Executable):
    def __init__(self, outer):
        self.outer = outer

    @classmethod
    def ThumbnailUnit(cls):
        logger.log("Created new ThumbnailUnit", section="Saveable")

        return ThumbnailUnit()
