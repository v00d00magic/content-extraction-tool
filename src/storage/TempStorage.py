from storage.StorageItem import StorageItem
from pathlib import Path
from utils.Data.Random import Random
import os

class TempStorage(StorageItem):
    def allocateTemp(self)->Path:
        rand_hash = Random().random_hash(64)

        rand_path = Path(os.path.join(self.dir, str(rand_hash)))
        rand_path.mkdir(exist_ok=True)

        return rand_path

    def subDir(self, dir: str):
        return TempStorage(self.root, "/".join([str(self.dir), dir]))
