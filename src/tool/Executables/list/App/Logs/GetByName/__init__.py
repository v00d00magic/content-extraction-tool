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
            return app.config.get("web.logs_watching.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        _file = args.get("file")

        if ".json" not in _file:
            _file = _file + ".json"

        logs_storage = app.logger.logs_storage
        dir_storage = logs_storage.dir

        log_file = dir_storage.joinpath(_file)

        assert log_file.is_file(), "not found"

        content = log_file.open().read()
        content_size = len(content)
        content_json = JSON(content).parse()

        return {
            "size": content_size,
            "logs": content_json,
        }
