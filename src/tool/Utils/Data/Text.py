from Utils.Util import Util
from App import app
import re

class Text(Util):
    def getValidName(self):
        '''
        Creates saveable name (removes forbidden ntfs characters)
        '''
        safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', self.data)
        safe_filename = re.sub(r'_+', '_', safe_filename)
        safe_filename = safe_filename.strip('_')
        if not safe_filename:
            return "unnamed"

        return safe_filename

    def cut(self, length: int = 100, multipoint: bool = True):
        newString = self.data[:length]

        if multipoint == False:
            return newString

        return newString + ("..." if self.data != newString else "")

    def cwdReplacement(self):
        self.replaceCwd(str(app.src))

        return self

    def replaceCwd(self, by):
        self.data = self.data.replace("?cwd?", by)

        return self
