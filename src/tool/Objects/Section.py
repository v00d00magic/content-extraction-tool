from Plugins.App.Storage.Storage import app

class Section:
    section_name = ["App"]

    def log(self, *args, **kwargs):
        kwargs["section"] = self.section_name

        return app.log(*args, **kwargs)

    def log_error(self, *args, **kwargs):
        return app.log(*args, **kwargs)

    def log_success(self, message):
        return app.log(message, kind="success")
