from Objects.Object import Object
from .StorageItem import StorageItem
from pathlib import Path
from Plugins.Data.Random import Random
from Utils.Data.JSON import JSON
import os

class StorageDirectory(Object):
    @classmethod
    def getHash(cls):
        HASH_BYTES = 32

        return Random().random_hash(HASH_BYTES)

    def __init__(self, storage: StorageItem, hash: str, do_mkdir: bool = False):
        self.do_mkdir: bool = do_mkdir
        self.storage: StorageItem = storage
        self.path = self.storage.path()
        self.hash: str = hash

        self.upper: Path = self.defineUpper()
        self.common: Path = self.defineCommon(self.upper)
        self.common_file: Path = None

    def defineUpper(self) -> Path:
        _dir = self.path.joinpath(self.hash[0:2])

        if self.do_mkdir == True:
            _dir.mkdir(exist_ok=True)

        return _dir

    def defineCommon(self, upper: Path) -> Path:
        _dir = upper.joinpath(self.hash)

        if self.do_mkdir == True:
            _dir.mkdir(exist_ok=True)

        return _dir

    def getProbalyCommonFile(self):
        return self.common.joinpath(self.hash).joinpath(self.hash)

    def setCommonFile(self, path: Path):
        self.common_file = path

    def renameCommonFile(self, new_name: str):
        new_name = Path(self.common.joinpath(new_name))
        self.common_file.rename(new_name)
        self.common_file = new_name

    def moveSelf(self, new_storage):
        _old = Path(self.common)

        self.path = new_storage.path()
        self.do_mkdir = True

        _new_name = self.path.joinpath(self.hash[0:2]).joinpath(self.hash)

        self.upper = self.defineUpper()
        _old.rename(_new_name)

        self.common = self.defineCommon(self.upper)
        self.setCommonFile(_new_name)

    def copySelf(self, new_storage):
        pass

    def generateFilesList(self):
        current_dir = self.common
        files_list = []

        for file in current_dir.rglob('*'):
            if file.is_file():
                files_list.append({
                    'path': str(file.relative_to(current_dir)),
                    'size': file.stat().st_size,
                    'name': file.name
                })

        return files_list

    def getPath(self):
        return self.path

    def getFilesList(self):
        return JSON(self.lists).parse()

    def getFilesSize(self):
        common_filesize = 0

        for file in self.Meta.getFilesList():
            common_filesize += file.get("size")

        return common_filesize
