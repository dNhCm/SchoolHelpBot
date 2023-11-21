import importlib
import os

from aiogram import Dispatcher

from misc.root import get_root, get_abspath


def register_routers(dp: Dispatcher):
    # Register middlewares of dispatcher (global middlewares)
    from .middlewares import register_dp_middlewares
    register_dp_middlewares(dp)

    # Include routers to dispatcher
    path = get_abspath(__file__)
    routers = os.listdir("/".join(path))
    routers.remove("__init__.py")
    routers.remove("__pycache__")
    routers.remove("middlewares")

    package = ".".join(path[len(get_root().split('/')):])
    for module in routers:
        import_get_router = importlib.import_module(f".{module}", package=package).get_router
        dp.include_router(import_get_router())
