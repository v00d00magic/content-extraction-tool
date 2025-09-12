from app.App import logger

class Sectionable():
    section_name = "App"

    KIND_SUCCESS = logger.KIND_SUCCESS
    KIND_ERROR = logger.KIND_ERROR
    KIND_DEPRECATED = logger.KIND_DEPRECATED
    KIND_MESSAGE = logger.KIND_MESSAGE

    def log(self, message, kind = "message"):
        return logger.log(message, section=self.section_name, kind=kind)
