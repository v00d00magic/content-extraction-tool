from executables.templates.representations import Representation

keys = {
    "arguments.name": {
        "en_US": "Passed data",
        "ru_RU": "Переданные данные"
    }
}

class Implementation(Representation):
    docs = {
        "name": keys.get("arguments.name"),
    }
