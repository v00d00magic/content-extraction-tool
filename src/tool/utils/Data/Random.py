import random
import secrets
from Utils.Util import Util

class Random(Util):
    def random_int(self, min, max):
        return random.randint(min, max)

    def random_hash(self, bytes = 32):
        return secrets.token_urlsafe(bytes)
