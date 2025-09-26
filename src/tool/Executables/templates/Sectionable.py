class Sectionable():
    section_name = "Executables"

    def log(self, *args, **kwargs):
        kwargs["section"] = self.section_name

        return self.call.log(*args, **kwargs)

    def log_error(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    def log_success(self, message):
        return self.log(message, kind="success")
