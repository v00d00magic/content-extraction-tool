from Objects.Outer import Outer

class Submodules(Outer):
    items: list = []
    external: list = []

    def get(self, type_in: list = None) -> list:
        if type_in != None:
            type_items = []
            for item in self.items:
                if item.self_name in type_in:
                    type_items.append(item)

            return type_items

        return self.items
