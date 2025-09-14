from urllib.parse import urlparse

class URL():
    def __init__(self, url):
        self._orig = url
        self.url = urlparse(url)

    def getExtension(self):
        path = self.url.path
        if path.endswith('/') or path == "":
            return "index", "html"
