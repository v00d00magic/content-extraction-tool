from executables.templates.outer import Outer

class Implementation(Outer):
    async def execute(self, i = {}):
        from PIL import Image as PILImage

        with PILImage.open(str(item.common_link.path())) as img:
            item.Outer.update({
                "width": img.size[0],
                "height": img.size[1],
            })

        return item
