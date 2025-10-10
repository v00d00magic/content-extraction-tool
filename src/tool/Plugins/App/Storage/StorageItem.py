from pydantic import Field
from Objects.Object import Object
from pathlib import Path

class StorageItem(Object):
    root: Path = Field(default=None)
    dir_name: str = Field(default=None)
    make_dir: bool = Field(default=True)

    def dir(self):
        return self.root.joinpath(self.dir_name)

    def constructor(self):
        if self.make_dir == True and self.dir().is_dir() == False:
            self.dir().mkdir()

    def extend(self, dir: str):
        return StorageItem(self.root, "/".join([str(self.dir()), dir]))

    def path(self):
        return self.dir()
