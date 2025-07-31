from mweb.engine.mweb_base import MWebBase
from mweb.engine.mweb_config import MWebConfig
from mweb.engine.mweb_data import MWebModuleDetails


class MWebRegistry:
    config: MWebConfig = None
    registerModules: dict[str, MWebModuleDetails] = {}
    mweb_app: MWebBase = None
    store: dict = {}

    @classmethod
    def add(cls, key: str, value):
        cls.store[key] = value

    @classmethod
    def get(cls, key: str, default=None):
        return cls.store.get(key, default)
