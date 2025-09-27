from Executables.Templates.Acts import Act

from App import app

class Implementation(Act):
    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return app.config.get("web.logs_watching.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, i = {}):
        log_files = app.logger.logs_storage.dir.glob('*.json')
        out_list = []
        
        for log_file in log_files:
            if log_file.is_file():
                out_list.append(log_file.name.replace(log_file.suffix, ""))

        # TODO convert to LogFile
        return out_list
