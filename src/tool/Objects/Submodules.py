from Objects.Outer import Outer

class Submodules(Outer):
    items: list = []
    external: list = []

    # Defined functions

    @property
    def submodules(self) -> dict:
        return {
            'items': [],
            'external': []
        }

    @property
    def manual_submodules(self) -> list:
        return []

    @property
    def all_submodules(self) -> list:
        return self.items + self.external

    def __init__(self, outer):
        super().__init__(outer)

        # Defined 'items' property will duplicate self to each new loaded Object, so workaround
        self.items = []
        self.external = []

        for key, val in self.submodules.items():
            if key not in ['items', 'external']:
                continue

            for item in val:
                getattr(self, key).append(item)

        for item in self.manual_submodules:
            if item in ["external_submodules", "internal_submodules"]:
                continue

            orig_item = getattr(self, item, None)
            val = getattr(orig_item, 'submodule_value', None)

            if None not in [val, orig_item]:
                if orig_item.submodule_value == 'internal':
                    self.items.append(orig_item)
                else:
                    self.external.append(orig_item)

    def _getList(self, list_in: list, type_in: list = None) -> list:
        if type_in != None:
            type_items = []
            for item in list_in:
                if item.self_name in type_in:
                    type_items.append(item)

            return type_items

        return list_in

    def getInternal(self, type_in: list = None):
        return self._getList(self.items, type_in)

    def getExternal(self, type_in: list = None):
        return self._getList(self.external, type_in)
