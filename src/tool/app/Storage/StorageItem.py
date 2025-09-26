from pathlib import Path
import os

class StorageItem:
    def __init__(self, root: str, dir_name: str = None, make_dir: bool = True):
        self.root = Path(root)
        self.dir_name = dir_name
        self.dir = self.root.joinpath(dir_name)

        if make_dir == True and self.dir.is_dir() == False:
            self.dir.mkdir()

    def extend(self, dir: str):
        return StorageItem(self.root, "/".join([str(self.dir), dir]))

    def path(self):
        return self.dir
