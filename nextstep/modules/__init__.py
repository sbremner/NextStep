from nextstep.core.errors import ModuleNameError

from .process import StartProcess
from .file import (
    CreateFile, ModifyFile, DeleteFile,
)
from .network import NetworkConnection

# Available modules
# TODO: Allow this dictionary to dynamically load from configured locations
MODULES = {
    'process.start': StartProcess(),
    'file.create': CreateFile(),
    'file.modify': ModifyFile(),
    'file.delete': DeleteFile(),
    'network.send': NetworkConnection(),
}


def get_modules():
    return MODULES


def load_module(module):
    """ Returns a module object back to the caller """
    available_modules = get_modules()

    if module not in available_modules:
        raise ModuleNameError("Invalid module name: {}".format(module))

    # TODO: Add validation that our module is a class maybe?
    return available_modules[module]