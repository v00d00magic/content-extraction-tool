from App import app
from pathlib import Path
from peewee import TextField, BigIntegerField, IntegerField, BooleanField
from Utils.Data.JSON import JSON
from Utils.Web.Mime import Mime
from DB.Models.Content.ContentModel import ContentModel
from App.Storage.HashDirectory import HashDirectory
from App.Logger.LogSection import LogSection

class StorageUnit(ContentModel):
    table_name = 'storage_units'
    self_name = 'StorageUnit'
    short_name = 'su'
    link_sign = "__$|su_"

    hash = TextField(null=True)
    # attached_path = TextField(null=True) i dont will add dis

    # it is about the main file!
    upload_name = TextField(null=False)
    extension = TextField(null=False)
    mime = TextField(null=True,default="N/A")
    filesize = BigIntegerField(default=0)
    metadata = TextField(default="")

    lists = TextField(default="")

    is_thumbnail = BooleanField(index=True,default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.isSaved() == False:
            self.hash = HashDirectory.getHash()
            self.tears(False)
        else:
            self.tears(True, False)

    def tears(self, as_saved = False, mkdir = True):
        if as_saved == False:
            self.hash_dir = HashDirectory(app.storage.get("temp_storage_units"), self.hash, mkdir)
        else:
            self.hash_dir = HashDirectory(app.storage.get("storage_units"), self.hash, mkdir)
            self.hash_dir.setCommonFile(self.hash_dir.getProbalyCommonFile())

    def getDir(self) -> Path:
        return self.hash_dir.common

    def getCommonFile(self) -> Path:
        return self.hash_dir.common_file

    def setDataFromPath(self, path: Path):
        self.filesize = path.stat().st_size

        if self.upload_name == None:
            self.setName((str(path.name), str(path.suffix[1:])))

    def setName(self, name_tuple):
        self.upload_name = name_tuple[0]
        self.extension = name_tuple[1]
        self.mime = Mime().getByName(self.upload_name)

    def setThumbnailMark(self):
        self.is_thumbnail = 1

    def setCommonFile(self, path: Path):
        self.hash_dir.setCommonFile(path)
        self.setDataFromPath(self.hash_dir.common_file)

    def renameCommonFile(self, name):
        self.hash_dir.renameCommonFile(name)

    def clearCommonFile(self):
        '''
        Changes file's name to ModelHash
        '''

        self.renameCommonFile(self.hash)

    def setFilesList(self, files_list):
        self.lists = JSON(files_list).dump()

    def getFilesList(self):
        return JSON(self.lists).parse()

    async def flush(self):
        assert self.hash_dir.common_file != None, "common_file not defined"

        self.setFilesList(self.hash_dir.generateFilesList())

        await super().flush()

        self.save(force_insert=True)

    def moveSelf(self):
        app.logger.log(f"Moving HashDirectory of StorageUnit {self.uuid} to storage_units", section = ["Saveable"])

        self.tears(False, False)
        self.hash_dir.moveSelf(app.storage.get("storage_units"))

    def getFileName(self):
        return ".".join([self.upload_name, self.extension])

    def getFilesSize(self):
        common_filesize = 0

        for file in self.getFilesList():
            common_filesize += file.get("size")

        return common_filesize

    def getStructure(self):
        app.logger.log(f"Getting API structure of {self.name_db_id}",section="Saveable")

        payload = {}
        payload['class_name'] = self.self_name
        payload['db'] = self.getDbName()
        payload["id"] = str(self.uuid)
        payload["name"] = {
            "upload_name": self.upload_name,
            "extension": self.extension,
        }
        payload["sizes"] = {
            "main": self.filesize,
            "dir": self.getFilesSize()
        }
        payload["hash"] = {
            "main": self.hash,
            "upper_hash": str(self.hash[0:2])
        }

        _rel_dir = self.hash_dir.storage.path()
        payload["path"] = {
            "upper": str(self.hash_dir.upper.relative_to(_rel_dir)),
            "common": str(self.hash_dir.common.relative_to(_rel_dir)),
            "common_file": str(self.hash_dir.common_file.relative_to(_rel_dir))
        }

        return payload
