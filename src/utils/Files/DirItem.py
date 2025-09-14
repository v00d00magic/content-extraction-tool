from pathlib import Path

class DirItem:
    def __init__(self, path):
        self.path = path

    def rmdir(self):
        '''
        better not to use
        '''
        path = Path(self.path)

        for sub in path.iterdir():
            if sub.is_dir():
                self.rmdir(sub)
            else:
                sub.unlink()

        path.rmdir()

    def dir_size(self):
        return sum(file.stat().st_size for file in Path(self.path).rglob('*'))
