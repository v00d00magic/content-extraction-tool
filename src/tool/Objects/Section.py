from App import app

class Section:
    @property
    def section_name(self) -> list:
        return ["App"]

    def log(self, *args, **kwargs):
        kwargs["section"] = self.section_name
        if kwargs.get("sections") != None:
            kwargs["section"] += kwargs.get("sections")

        return app.Logger.log(*args, **kwargs)

    def log_error(self, *args, **kwargs):
        return app.Logger.log(*args, **kwargs)

    def log_success(self, message):
        return app.Logger.log(message, kind="success")
