import os, json
from app.App import logger, storage
from pathlib import Path
from peewee import TextField, BigIntegerField, IntegerField, BooleanField
from utils.MainUtils import dump_json, parse_json, get_random_hash
from db.Models.Content.ContentModel import BaseModel
from submodules.Files.FileManager import file_manager
import shutil, mimetypes

class StorageUnit(BaseModel):
    table_name = 'storage_units'
    self_name = 'StorageUnit'
    short_name = 'su'
    temp_dir = None
    path_link = None

    # Identification
    hash = TextField(null=True)
    attached_path = TextField(null=True)

    upload_name = TextField(default='N/A') # Upload name (with extension)
    extension = TextField(default="json") # File extension
    mime = TextField(null=True,default="N/A")
    is_thumbnail = BooleanField(index=True,default=0)

    # Sizes
    filesize = BigIntegerField(default=0) # Size of main file

    # Probaly
    lists = TextField(default="")
    metadata = TextField(default="")

    @property
    def dir_filesize(self):
        maps = parse_json(self.lists)
        common_filesize = 0

        for file in maps:
            common_filesize += file.get("size")

        return common_filesize

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.is_saved() == False:
            self.temp_dir = storage.sub('tmp_files').allocateTemp()

    def removeTemp(self):
        # get cursed
        if self.temp_dir != None:
            file_manager.rmdir(self.temp_dir)

    def generateHash(self):
        self.hash = get_random_hash(32)

    def flush(self):
        self.generateFilesList()
        self.save(force_insert=True)
        self.moveTempDir()

    def setMime(self):
        _mime = mimetypes.guess_type(self.path())
        self.mime = _mime[0]

    def generateFilesList(self):
        _p = Path(self.temp_dir)
        _files = _p.rglob('*')
        _map = []

        for file in _files:
            if file.is_file():
                _map.append({
                    'path': str(file.relative_to(_p)),
                    'size': file.stat().st_size,
                    'name': file.name
                })

        self.lists = dump_json(_map)

    def setAbout(self):
        path = self.path_link

        file_stat = path.stat()
        self.filesize = file_stat.st_size
        self.extension = str(path.suffix[1:])
        self.upload_name = str(path.name)

    def setMainFile(self, path: Path):
        self.path_link = Path(path)
        self.generateHash()
        self.setAbout()
        self.setMime()
        self.flush()

    def setLink(self, link):
        self.path_link = Path(link)
        self.link = str(link)

    def markAsPreview(self):
        self.is_thumbnail = 1

    def writeData(self, json_data):
        self.extension = json_data.get("extension")

        if json_data.get("hash") == None:
            self.hash = get_random_hash(32)
        else:
            self.hash = json_data.get("hash")

        self.upload_name = json_data.get("upload_name")
        self.filesize = json_data.get("filesize")
        self.setMime()

        # broken function
        if json_data.get("link") != None:
            self.link = json_data.get("link")

        ''' TODO handle async
        if json_data.get("take_metadata", False) == True:
            self.fillMeta()'''

        self.flush()

    def moveTempDir(self):
        '''
        Renames temp directory to new hash dir and changes main file name to hash
        '''
        if self.temp_dir == None:
            return 

        temp_dir = Path(self.temp_dir)

        current_path = Path(os.path.join(str(temp_dir), self.upload_name))
        new_name = Path(os.path.join(str(temp_dir), f"{'.'.join([str(self.hash), self.extension])}"))

        current_path.rename(str(new_name))

        new_storage_category = storage.sub('files').allocateHash(self.hash, only_return=True)
        temp_dir.rename(str(new_storage_category))
        
        self.temp_dir = None

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
            "dir": self.dir_filesize
        }
        payload["hash"] = {
            "main": self.hash,
            "upper_hash": str(self.upper_hash_dir())
        }
        payload["path"] = {
            "dir": str(self.dir_path()),
            "main": str(self.path()),
            "relative_dir": self.relative_dir_path(),
            "relative_main": self.relative_main_file_path(),
        }

        return payload

    def path(self):
        if getattr(self, "attached_path", None) != None:
            return self.attached_path

        __path = os.path.join(storage.sub('files').path(), self.hash[0:2])
        __end_dir = os.path.join(__path, self.hash)
        if self.temp_dir != None:
            __end_dir = self.temp_dir

        __path = os.path.join(__end_dir, str(self.hash_filename()))

        return Path(__path)

    def hash_filename(self):
        if self.temp_dir != None:
            return f"{self.upload_name}"

        return f"{self.hash}.{str(self.extension)}"

    def upper_hash_dir(self):
        return Path(os.path.join(storage.sub('files').path(), str(self.hash[0:2])))

    def dir_path(self, need_check = False):
        __dir_path = Path(os.path.join(storage.sub('files').path(), str(self.hash[0:2]), self.hash))

        if need_check == True and __dir_path.exists() == False:
            __dir_path.mkdir(parents=True)

        return __dir_path

    def relative_dir_path(self):
        return f"{str(self.hash[0:2])}/{self.hash}"

    def relative_main_file_path(self):
        _p = self.relative_dir_path()

        return f"{_p}/{self.hash_filename()}"
