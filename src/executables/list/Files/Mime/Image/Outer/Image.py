from executables.templates.outer import Outer

class Implementation(Outer):
    async def implementation(self, i = {}):
        from PIL import Image as PILImage

        item = i.get("item")

        with PILImage.open(str(item.common_link.Path.getMainFilePath())) as img:
            item.JSONContent.update({
                "width": img.size[0],
                "height": img.size[1],
            })
