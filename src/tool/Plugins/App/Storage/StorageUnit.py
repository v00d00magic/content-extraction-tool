from Plugins.DB.Content.ContentUnit import ContentUnit

class StorageUnit(ContentUnit):
    class ContentData(ContentUnit.ContentData):
        hash: str
        upload_name: str
        ext: str
        mime: str
        common_size: int
        files: list

        it_thumbnail: bool = False

    content: ContentData
