from app.App import logger

class Sectionable():
    section_name = "App"

    def log(self, message, kind = "message"):
        return logger.log(message, section=self.section_name, kind=kind)

    def log_error(self, message):
        return self.log(message, kind=logger.KIND_ERROR)

    def log_success(self, message):
        return self.log(message, kind=logger.KIND_SUCCESS)
