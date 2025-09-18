import os, json
from app.App import logger, storage
from pathlib import Path
from peewee import TextField, BigIntegerField, IntegerField, BooleanField
from utils.Files.DirItem import DirItem
from utils.Data.JSON import JSON
from utils.Data.Random import Random
from db.Models.Content.ContentModel import ContentModel
import shutil, mimetypes

class StorageUnit(ContentModel):
    table_name = 'storage_units'
    self_name = 'StorageUnit'
    short_name = 'su'

    hash = TextField(null=True)
    # attached_path = TextField(null=True) i dont will add dis

    # it is about the main file!
    upload_name = TextField(default="N/A")
    extension = TextField(default="json")
    mime = TextField(null=True,default="N/A")
    filesize = BigIntegerField(default=0)
    metadata = TextField(default="")

    # it is about 
    lists = TextField(default="")

    is_thumbnail = BooleanField(index=True,default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        class Temp:
            @classmethod
            def get(cls):
                return self._temp_dir

            @classmethod
            def allocate(cls):
                return storage.get('tmp_files').allocateTemp()

            @classmethod
            def remove(cls):
                # Do not use
                if self._temp_dir != None:
                    DirItem(self._temp_dir).rmdir()

            @classmethod
            def detempize(cls):
                if self._temp_dir == None:
                    return 

                current_path = self._temp_dir.joinpath(self.upload_name)
                new_name = self._temp_dir.joinpath('.'.join([str(self.hash), self.extension]))

                current_path.rename(str(new_name))

                new_storage_category = storage.get('files').allocateHash(self.hash, only_return=True)
                self._temp_dir.rename(str(new_storage_category))

                self._temp_dir = None

        class Meta:
            @classmethod
            def generateFilesList(cls):
                current_dir = self.getCurrentDir()
                files_list = []

                for file in current_dir.rglob('*'):
                    if file.is_file():
                        files_list.append({
                            'path': str(file.relative_to(current_dir)),
                            'size': file.stat().st_size,
                            'name': file.name
                        })

                return files_list

            @classmethod
            def getFilesList(cls):
                return JSON.parse(self.lists)

            @classmethod
            def getFilesSize(cls):
                common_filesize = 0

                for file in self.Meta.getFilesList():
                    common_filesize += file.get("size")

                return common_filesize

        class Path:
            @classmethod
            def getStorage(cls):
                return storage.get('files').path()

            @classmethod
            def getUpper(cls):
                return cls.getStorage().joinpath(self.hash[0:2])

            @classmethod
            def getCommon(cls, need_check = True, relative = False):
                _ret = cls.getUpper().joinpath(self.hash)
                #if self._temp_dir != None:
                #    return self._temp_dir

                if need_check == True and _ret.exists() == False:
                    _ret.mkdir(parents=True)

                if relative == True:
                    return _ret.relative_to(cls.getStorage())

                return _ret

            @classmethod
            def getMainFilePath(cls, relative = False):
                _ret = cls.getCommon().joinpath(str(cls.getFilename()))

                if relative == True:
                    return _ret.relative_to(cls.getStorage())

                return _ret

            @classmethod
            def getFilename(cls):
                if self._temp_dir != None:
                    return f"{self.upload_name}"

                return f"{self.hash}.{str(self.extension)}"

        self._temp_dir = None
        self._path_link = None
        self.hash = Random().random_hash(32)

        self.Temp = Temp()
        self.Meta = Meta()
        self.Path = Path()

        if self.isSaved() == False:
            self._temp_dir = self.Temp.allocate()

    def getCurrentDir(self):
        if self._temp_dir != None:
            return self._temp_dir

    def flush(self):
        self.lists = JSON(self.Meta.generateFilesList()).dump()
        self.save(force_insert=True)
        self.Temp.detempize()

    def markAsPreview(self):
        self.is_thumbnail = 1

    def getMime(self, name):
        _mime = mimetypes.guess_type(name)
        return _mime[0]

    def linkPath(self, path: Path):
        self._path_link = Path(path)
        self.fillByPath(self._path_link)
        self.flush()

    def fillByPath(self, path):
        self.filesize = path.stat().st_size
        self.extension = str(path.suffix[1:])
        self.upload_name = str(path.name)
        self.mime = self.getMime(self.upload_name)

    def fillByJson(self, json_data):
        self.extension = json_data.get("extension")
        self.upload_name = json_data.get("upload_name")
        self.filesize = json_data.get("filesize")
        self.mime = self.getMime(self.upload_name)

        ''' TODO handle async
        if json_data.get("take_metadata", False) == True:
            self.fillMeta()'''

        self.flush()

    def getStructure(self):
        payload = {}
        payload['class_name'] = self.self_name
        payload["id"] = str(self.uuid)
        payload["name"] = {
            "upload_name": self.upload_name,
            "extension": self.extension,
        }
        payload["sizes"] = {
            "main": self.filesize,
            "dir": self.Meta.getFilesSize()
        }
        payload["hash"] = {
            "main": self.hash,
            "upper_hash": str(self.hash[0:2])
        }
        payload["path"] = {
            "relative_dir": str(self.Path.getCommon(relative=True)),
            "relative_main": str(self.Path.getMainFilePath(relative=True))
        }

        return payload
