from Objects.Outer import Outer

class Submodules(Outer):
    usage_items: list = []
    usage_external: list = []

    @property
    def all_submodules(self) -> list:
        return self.usage_items + self.usage_external

    @property
    def manual_submodules(self) -> list:
        return []

    def __init__(self, outer):
        super().__init__(outer)

        for item in self.manual_submodules:
            if item in ["external_submodules", "internal_submodules"]:
                continue

            orig_item = getattr(self, item, None)
            val = getattr(orig_item, 'submodule_value', None)

            if None not in [val, orig_item]:
                if orig_item.submodule_value == 'internal':
                    self.usage_items.append(orig_item)
                else:
                    self.usage_external.append(orig_item)

    def _getList(self, list_in: list, type_in: list = None) -> list:
        if type_in != None:
            type_items = []
            for item in list_in:
                if item.self_name in type_in:
                    type_items.append(item)

            return type_items

        return list_in

    def getInternal(self, type_in: list = None):
        return self._getList(self.usage_items, type_in)

    def getExternal(self, type_in: list = None):
        return self._getList(self.usage_external, type_in)
