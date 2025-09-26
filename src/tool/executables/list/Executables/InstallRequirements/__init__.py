from Executables.templates.acts import Act
from Declarable.Arguments import ExecutableArgument
import subprocess, sys

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["class"] = ExecutableArgument({
            "assertion": {
                "not_null": True
            }
        })

        return params

    async def implementation(self, i = {}):
        _class = i.get("class")
        _need_modules = _class.getRequiredModules()

        if len(_need_modules) > 0:
            _pars = [sys.executable, '-m', 'pip', 'install']
            for _module in _need_modules:
                _pars.append(_module)

            subprocess.call(_pars)

        return {
            "modules": _need_modules
        }
