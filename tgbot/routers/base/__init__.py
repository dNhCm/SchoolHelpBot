import importlib
import os

from aiogram import Router

from misc.root import get_root
from .middlewares import register_middlewares
from .handlers import register_handlers
from .errors import register_errors


def get_router() -> Router:
    router = Router(name=os.path.basename(os.getcwd()))

    # Register middlewares, handlers and errors
    register_middlewares(router)
    register_handlers(router)
    register_errors(router)

    # Include to router another routers
    path = os.path.abspath(__file__).split('\\')[:-1]
    path.append("routers")
    try:
        routers = os.listdir("\\".join(path))

        for module in routers:
            import_get_router = importlib.import_module(f".{module}", package=".".join(path[len(get_root()):])).get_router
            router.include_router(import_get_router())
    except (FileNotFoundError, TypeError):
        pass

    return router
