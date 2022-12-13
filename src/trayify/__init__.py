from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "1.1.0"

_cfg = tomllib.loads(resources.read_text("trayify", "config.toml"))