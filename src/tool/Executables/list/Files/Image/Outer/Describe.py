from Executables.Templates.Outer import Outer

class Implementation(Outer):
    async def implementation(self, i = {}):
        from PIL import Image as PILImage

        item = i.get("item")

        for common_item in item.LinkManager.getCommon():
            with PILImage.open(common_item.getCommonFile()) as img:
                item.JSONContent.update({
                    "image": {
                        "width": img.size[0],
                        "height": img.size[1],
                    }
                })
