from declarable.Arguments import StringArgument, LimitedArgument, CsvArgument
from .. import Implementation as File
from submodules.Files.FileManager import file_manager
from pathlib import Path
import os

locale_keys = {
    "path.name": {
        "en_US": "Path to file",
        "ru_RU": "Путь к файлу"
    },
    "type.name": {
        "en_US": "Text",
        "ru_RU": "Текст"
    },
    "type.copy.name": {
        "en_US": "Copy",
        "ru_RU": "Копирование",
    },
    "type.move.name": {
        "en_US": "Move",
        "ru_RU": "Перемещение",
    },
    "type.link.name": {
        "en_US": "Link",
        "ru_RU": "Ссылка",
    }
}

class Implementation(File.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["path"] = CsvArgument({
            "orig": StringArgument({}),
            "docs": {
                "name": cls.key("path.name"),
            },
        })
        params["type"] = LimitedArgument({
            "docs": {
                "name": cls.key("type.name"),
                "values": {
                    "copy": {
                        "name": cls.key("type.copy.name")
                    },
                    "move": {
                        "name": cls.key("type.move.name")
                    },
                    "link": {
                        "name": cls.key("type.link.name")
                    },
                }
            },
            "values": ["copy", "move", "link"],
            "default": "copy",
        })

        return params

    async def implementation(self, i = {}):
        outs = []

        for _path in i.get('path'):
            path = Path(_path)
            file_name = path.name

            assert path.exists(), 'path does not exists'
            assert path.is_dir() == False, 'path is dir'
            assert i.get("type") in ['copy', 'move', 'link'], 'invalid type'

            out = self.ContentUnit()
            file = self.StorageUnit()

            move_to = Path(os.path.join(file.temp_dir, file_name))

            match(i.get("type")):
                case "copy":
                    file_manager.copyFile(path, move_to)
                    file.setMainFile(move_to)
                case "move":
                    file_manager.moveFile(path, move_to)
                    file.setMainFile(move_to)

            out.link(file, True)
            out.display_name = file_name
            out.JSONContent.update({
                "exported": str(i.get("type")),
                "format": str(path.suffix[1:]),
            })
            out.Source.update({
                "type": "path",
                "content": str(path)
            })
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
