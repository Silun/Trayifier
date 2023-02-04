import sys
from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "1.2.0"

assert sys.platform == "win32", "Trayify only works on the win32 platform."

_cfg = tomllib.loads(resources.read_text("trayify", "config.toml"))