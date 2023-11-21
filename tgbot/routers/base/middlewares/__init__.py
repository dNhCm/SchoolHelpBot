
import importlib
import os

from aiogram import Router

from misc.root import get_root, get_abspath


def register_middlewares(router: Router):
    path = get_abspath(__file__)
    modules: list[str] = list(map(lambda x: x[:-3], os.listdir("/".join(path))))
    modules.remove('__init__')
    modules.remove('__pycach')

    package = ".".join(path[len(get_root().split('/')):])
    for module in modules:
        import_register = importlib.import_module(f".{module}", package=package).register
        import_register(router)
