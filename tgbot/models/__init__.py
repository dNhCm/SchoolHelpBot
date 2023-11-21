import importlib
import os

from misc.root import get_root, get_abspath


async def connect_models():
    path = get_abspath(__file__)
    python_models = os.listdir("/".join(path))

    for el in python_models:
        if not el[-3:] == ".py":
            python_models.remove(el)
    python_models.remove("__init__.py")
    python_models = list(map(lambda x: x[:-3], python_models))

    package = ".".join(path[len(get_root().split('/')):])
    for module in python_models:
        import_connect = importlib.import_module(f".{module}", package=package).main
        await import_connect()
