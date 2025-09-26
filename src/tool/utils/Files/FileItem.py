from pathlib import Path
import os, shutil

class FileItem():
    def __init__(self, path):
        self.path = path

    def write(self, content, write_mode = "w"):
        stream = open(self.path, write_mode, encoding='utf-8')
        stream.write(content)
        stream.close()

    def move(self, to):
        shutil.move(str(self.path), str(to))
    
    def copy(self, to):
        shutil.copy2(str(self.path), str(to))

    def symlink(self, to):
        os.symlink(str(self.path), str(to))

    def copytree(self, src, dst, symlinks = False, ignore = None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
