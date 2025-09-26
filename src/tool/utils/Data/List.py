from utils.Util import Util

class List(Util):
    def convert(self):
        if type(self.data) != list:
            return [self.data]

        return self.data
