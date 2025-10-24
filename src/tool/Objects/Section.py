from Plugins.App.Logger.LogParts.LogKind import LogKindEnum
from Plugins.App.Logger.LogParts.LogPrefix import LogPrefix
from App import app

class Section:
    @property
    def section_name(self) -> list:
        # it implies that you have extended Object
        return self.meta.name

    @property
    def prefix(self) -> LogPrefix:
        return None

    def log(self, *args, **kwargs):
        kwargs["section"] = self.section_name
        if kwargs.get("sections") != None:
            kwargs["section"] += kwargs.get("sections")
        
        if self.prefix != None:
            kwargs["prefix"] = self.prefix

        return app.Logger.log(*args, **kwargs)

    def log_error(self, *args, **kwargs):
        kwargs["kind"] = LogKindEnum.error.value
        return self.log(*args, **kwargs)

    def log_success(self, *args, **kwargs):
        kwargs["kind"] = LogKindEnum.success.value
        return self.log(*args, **kwargs)
