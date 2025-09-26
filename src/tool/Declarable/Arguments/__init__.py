from pathlib import Path
import importlib, pkgutil, os
import sys

def _load_classes():
    __all__ = []

    arguments_module = sys.modules.setdefault(
        'Declarable.Arguments', 
        type(sys)('declarable.Arguments')
    )
    # app.cwd should be
    arguments_dir = Path(os.getcwd()).joinpath("Declarable").joinpath("Arguments")

    for argument_item in arguments_dir.rglob('*Argument.py'):
        class_path = argument_item.relative_to(arguments_dir)
        class_path = class_path.with_suffix("")
        class_name = ".".join(class_path.parts)

        _imported = importlib.import_module("Declarable.Arguments." + class_name)
        _class = getattr(_imported, class_path.parts[-1])
        __all__.append(_class)

        setattr(arguments_module, class_path.parts[-1], _class)
    
    arguments_module.__all__ = __all__
    sys.modules['Declarable.Arguments'] = arguments_module

_load_classes()
