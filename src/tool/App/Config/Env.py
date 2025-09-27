from App.Config import Config

class Env(Config):
    file_name = "env.json"
    fallback = None

    @classmethod
    def declareSettings(cls):
        from Declarable.Arguments import BooleanArgument

        items = {}
        items["env.external_editing.allow"] = BooleanArgument({
            "default": False,
        })

        return items
