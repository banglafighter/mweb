from mweb.engine.mweb_base import MWebBase
from mweb.engine.mweb_config import MWebConfig
from mweb.engine.mweb_data import MWebModuleDetails


class MWebRegistry:
    config: MWebConfig = None
    registerModules: dict[str, MWebModuleDetails] = {}
    mweb_app: MWebBase = None
