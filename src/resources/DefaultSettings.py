from declarable.Arguments import Argument, StringArgument, IntArgument, BooleanArgument, LimitedArgument, CsvArgument
from declarable.Documentation import documentation

locale_keys = {
    "ui.lang.name": {
        "en_US": "Language",
    },
    "ui.name.name": {
        "en_US": "Server name",
    },
    "web.host.name": {
        "en_US": "Host name",
    },
    "web.port.name": {
        "en_US": "Port",
    },
    "storage.root_path.name": {
        "en_US": "Storage location",
    },
    "storage.root_path.definition": {
        "en_US": "Internal storage location. «?cwd?» is replaced with the startup directory. Edit with caution.",
    },
    "net.max_speed.name": {
        "en_US": "Max speed",
    },
    "net.useragent.name": {
        "en_US": "User-Agent",
    },
    "net.max_speed.definition": {
        "en_US": "Max speed for web operations (in Kbps)",
    },
    "net.timeout.name": {
        "en_US": "Timeout",
    },
    "net.timeout.definition": {
        "en_US": "Timeout for web operations",
    },
    "logger.skip_categories.name": {
        "en_US": "Ignored categories",
    },
    "logger.skip_categories.definition": {
        "en_US": "List of categories that will not be displayed from the logger",
    },
    "logger.skip_file.name": {
        "en_US": "Do not write logs into the file",
    },
    "thumbnail.width.name": {
        "en_US": "Thumbnail width",
    },
    "thumbnail.height.name": {
        "en_US": "Thumbnail height",
    }
}

documentation.loadKeys(locale_keys)

DefaultSettings = {
    "ui.lang": StringArgument({
        "default": 'en_US',
        "docs": {
            "name": documentation.get("ui.lang.name"),
        },
    }),
    "ui.name": StringArgument({
        "default": "Content extraction tool",
        "docs": {
            "name": documentation.get("ui.name.name"),
        },
    }),
    "web.config_editing.allow": BooleanArgument({ # Allow to edit config from web
        "default": True,
    }),
    "web.env_editing.allow": BooleanArgument({ # Allow to edit env variables from web
        "default": False,
    }),
    "web.logs_watching.allow": BooleanArgument({
        "default": True,
    }),
    "web.host": StringArgument({
        "default": "127.0.0.1",
        "docs": {
            "name": documentation.get("web.host.name"),
        },
    }),
    "web.port": IntArgument({
        "default": 26666,
        "docs": {
            "name": documentation.get("web.port.name"),
        },
    }),
    "web.debug": BooleanArgument({
        "default": True,
    }),
    "storage.root_path": StringArgument({
        "default": "?cwd?/storage", # cwd -> /storage
        "docs": {
            "name": documentation.get("storage.root_path.name"),
            "definition": documentation.get("storage.root_path.definition"),
        },
    }),
    "db.content.connection": StringArgument({
        "default": "sqlite:///?cwd?/storage/dbs/content.db"
    }),
    "db.instance.connection": StringArgument({
        "default": "sqlite:///?cwd?/storage/dbs/instance.db"
    }),
    "net.max_speed": IntArgument({
        "default": 2000, # kbs
        "docs": {
            "name": documentation.get("net.max_speed.name"),
            "definition": documentation.get("net.max_speed.definition"),
        },
    }),
    "net.useragent": StringArgument({
        "default": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        "docs": {
            "name": documentation.get("net.useragent.name"),
        },
    }),
    "net.timeout": IntArgument({
        "default": 100,
        "docs": {
            "name": documentation.get("net.timeout.name"),
            "definition": documentation.get("net.timeout.definition"),
        },
    }),
    "logger.skip_categories": CsvArgument({
        "default": [{
            "name": "ExecutableMap",
            "wildcard": True,
            "kinda": "message",
            "where": "cli"
        }],
        "orig": Argument({
            "tip": ["name", "where", "wildcard", "kinda"]
        }),
        "docs": {
            "name": documentation.get("logger.skip_categories.name"),
            "definition": documentation.get("logger.skip_categories.definition"),
        },
    }),
    "logger.skip_file": BooleanArgument({
        "default": 0,
        "docs": {
            "name": documentation.get("logger.skip_file.name"),
        },
    }),
    "thumbnail.width": IntArgument({
        "default": 200,
        "docs": {
            "name": documentation.get("thumbnail.width.name"),
        },
    }),
    "thumbnail.height": IntArgument({
        "default": 200,
        "docs": {
            "name": documentation.get("thumbnail.width.height"),
        },
    }),
}
