from utils.Util import Util
from datetime import datetime

class Date(Util):
    def timestamp_or_float(self):
        if self.data == None:
            return None

        if getattr(self.data, 'timestamp', None) != None:
            return float(self.data.timestamp())
        else:
            return float(self.data)

    def now(self):
        return datetime.now().timestamp()
