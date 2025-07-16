from mweb.engine.mweb_hook import MWebHook
from .mweb_saas_connector import MWebExternalSaaSConfig


class MWebSaaSRegistry:
    _in_memory_config: dict[str, dict] = {}

    @classmethod
    def set_config(cls, tenant_key: str, config_key: str, value):
        ex_config: MWebExternalSaaSConfig | None = MWebHook.external_saas_config()
        if ex_config is not None:
            ex_config.set_config(tenant_key=tenant_key, config_key=config_key, value=value)
        else:
            cls._in_memory_config.setdefault(tenant_key, {})[config_key] = value

    @classmethod
    def get_config(cls, config_key: str, default=None, tenant_key: str = None):
        ex_config: MWebExternalSaaSConfig | None = MWebHook.external_saas_config()
        if ex_config is not None:
            return ex_config.get_config(tenant_key=tenant_key, config_key=config_key, default=default)
        else:
            return cls._in_memory_config.get(tenant_key, {}).get(config_key, default)
