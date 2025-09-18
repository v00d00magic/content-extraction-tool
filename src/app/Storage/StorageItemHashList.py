from app.Storage.StorageItem import StorageItem
from pathlib import Path
from utils.Data.Random import Random
import os

class StorageItemHashList(StorageItem):
    def allocateHash(self, hash, only_return = True):
        __main_hash_path = os.path.join(self.dir, hash[0:2])
        os.makedirs(__main_hash_path, exist_ok=True)

        __hash_path = os.path.join(__main_hash_path, hash)
        if only_return == True:
            return Path(__hash_path)

        os.makedirs(__hash_path, exist_ok=True)

        return Path(__hash_path)

    def allocateHashOnce(self, hash):
        __main_hash_path = os.path.join(self.dir, hash)
        os.makedirs(__main_hash_path, exist_ok=True)

        return Path(__main_hash_path)

    def allocateTemp(self)->Path:
        rand_hash = Random().random_hash(64)

        rand_path = Path(os.path.join(self.dir, str(rand_hash)))
        rand_path.mkdir(exist_ok=True)

        return rand_path

    def subDir(self, dir: str):
        return TempStorage(self.root, "/".join([str(self.dir), dir]))
