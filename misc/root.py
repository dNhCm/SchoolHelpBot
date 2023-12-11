import os.path


def get_root() -> str:
    root = os.path.abspath(__file__).split('/')
    if len(root) == 1:
        root = os.path.abspath(__file__).split('\\')

    return "/".join(root[:-2])


def get_abspath(file: __file__) -> str:
    return (
        os.path.abspath(file).split('\\')[:-1]
        if len(os.path.abspath(file).split('/')) == 1
        else os.path.abspath(file).split('/')[:-1]
    )
