from db.Models.Content.StorageUnit import StorageUnit

# Pseudo model that represents thumbnail
class ThumbnailState():
    data = {}

    def __init__(self, json):
        self.write(json)

    def write(self, json):
        self.data = json

    def state(self):
        return self.data

    def getStructure(self):
        data = self.state()
        su = StorageUnit.ids(data.get("storage_unit_id"))

        if su:
            data["storage_unit"] = su.getStructure()

        return data
