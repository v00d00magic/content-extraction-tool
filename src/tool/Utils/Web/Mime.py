import mimetypes

class Mime():
    def getByName(self, name):
        _mime = mimetypes.guess_type(name)

        return _mime[0]
