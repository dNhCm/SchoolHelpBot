
import os


def get_project_path() -> str:
    current_path = os.path.abspath(__file__).split('\\')
    index = current_path.index('SchoolHelpBot')
    return '\\'.join(current_path[:index + 1])