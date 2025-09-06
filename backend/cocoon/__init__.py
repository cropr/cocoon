import toml
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def read_version():
    with open("pyproject.toml") as f:
        mt = toml.load(f)
        return mt["project"]["version"]


version = read_version()
