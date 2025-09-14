class ThumbnailMixin():
    def saveThumbnail(self, method):
        return {}
        thumb_class = method.outer.Thumbnail(method)
        thumb_out = thumb_class.create(self, {})

        return thumb_out

    def setThumbnail(self, thumbs):
        thumbs_out = []

        if thumbs:
            for __ in thumbs:
                thumbs_out.append(__.state())

        write_this = {}
        if len(thumbs_out) > 0:
            write_this["thumbnail"] = thumbs_out

        self.Outer.update(write_this)
