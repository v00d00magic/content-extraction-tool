from declarable.Arguments import StringArgument, LimitedArgument, CsvArgument
from utils.Files.FileItem import FileItem
from .. import Implementation as File
from pathlib import Path
import os

locale_keys = {
    "path.name": {
        "en_US": "Path to file",
    },
    "type.name": {
        "en_US": "Text",
    },
    "type.copy.name": {
        "en_US": "Copy",
    },
    "type.move.name": {
        "en_US": "Move",
    },
    "type.link.name": {
        "en_US": "Link",
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

            out_file = self.StorageUnit()
            move_to = out_file.getDir().joinpath(file_name)

            match(i.get("type")):
                case "copy":
                    FileItem(path).copy(move_to)
                case "move":
                    FileItem(path).move(move_to)

            out_file.setCommonFile(move_to)
            await out_file.flush()

            out = self.ContentUnit()
            out.display_name = out_file.getFileName()
            out.JSONContent.update({
                "exported": str(i.get("type")),
                "format": str(path.suffix[1:]),
            })
            out.Source.update({
                "type": "path",
                "content": str(path)
            })
            await out.flush()
            out.LinkManager.linkAsCommon(out_file)

            outs.append(out)

        return outs
