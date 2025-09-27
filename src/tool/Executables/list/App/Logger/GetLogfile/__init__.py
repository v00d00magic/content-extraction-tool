from Declarable.Arguments import StringArgument
from Utils.Data.JSON import JSON
from Executables.Templates.Acts import Act
from App import app

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["file"] = StringArgument({
            "default": None,
            "assertion": {
                "not_null": True
            }
        })

        return params

    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return app.config.get("logger.external_watching.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        file = args.get("file")
        if ".json" not in file:
            file = file + ".json"

        log_file = app.logger.logs_storage.dir.joinpath(file)

        assert log_file.is_file(), "file not found"

        content = log_file.open().read()
        content_size = len(content)
        content_json = JSON(content).parse()

        # TODO convert to LogMessage's

        return {
            "size": content_size,
            "logs": content_json,
        }
