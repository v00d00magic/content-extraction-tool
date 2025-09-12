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
            "default": None,
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
        pathes = i.get('path')
        outs = []

        for _path in pathes:
            path = Path(_path)
            move_type = i.get("type")
            link = None

            assert path.exists(), 'path does not exists'
            assert path.is_dir() == False, 'path is dir'
            assert move_type in ['copy', 'move', 'link'], 'invalid type'

            out = self.ContentUnit()
            su = self.StorageUnit()

            file_name = path.name
            move_to = Path(os.path.join(su.temp_dir, file_name))

            match(move_type):
                case "copy":
                    file_manager.copyFile(path, move_to)
                    su.setMainFile(move_to)
                case "move":
                    file_manager.moveFile(path, move_to)
                    su.setMainFile(move_to)
                case "link":
                    su.setLink(link)
                    #file_manager.symlinkFile(INPUT_PATH, MOVE_TO)

            out.addLink(su)
            out.setCommonLink(su)
            out.display_name = file_name
            out.content = {
                "export_as": str(move_type),
                "format": str(path.suffix[1:]),
            }
            out.source = {
                "type": "path",
                "content": str(path)
            }
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
