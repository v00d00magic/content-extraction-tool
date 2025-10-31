from Objects.Outer import Outer

class Submodules(Outer):
    usage_items: list = []
    usage_external: list = []

    @property
    def internal_submodules(self):
        return self.usage_items + self._getSubclassModules('internal')

    @property
    def external_submodules(self):
        return self.usage_external + self._getSubclassModules('external')

    def _getSubclassModules(self, by_submodule_value: str) -> list:
        output = []
        for item in dir(self):
            if item in ["external_submodules", "internal_submodules"]:
                continue

            orig_item = getattr(self, item, None)
            val = getattr(orig_item, 'submodule_value', None)

            if None not in [val, orig_item]:
                if by_submodule_value != None and by_submodule_value == val:
                    output.append(orig_item)

        return output

    def _getList(self, list_in: list, type_in: list = None) -> list:
        if type_in != None:
            type_items = []
            for item in list_in:
                if item.self_name in type_in:
                    type_items.append(item)

            return type_items

        return list_in

    def getInternal(self, type_in: list = None):
        return self._getList(self.internal_submodules, type_in)

    def getExternal(self, type_in: list = None):
        return self._getList(self.external_submodules, type_in)
