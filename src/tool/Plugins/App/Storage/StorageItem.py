from pydantic import Field
from Objects.Object import Object
from pathlib import Path

class StorageItem:
    root: Path = Field()
    dir_name: str = Field()

    def dir(self):
        return self.root.joinpath(self.dir_name)

    def __init__(self, root: str, dir_name: str = None, make_dir: bool = True):
        if make_dir == True and self.dir.is_dir() == False:
            self.dir().mkdir()

    def extend(self, dir: str):
        return StorageItem(self.root, "/".join([str(self.dir()), dir]))

    def path(self):
        return self.dir()
