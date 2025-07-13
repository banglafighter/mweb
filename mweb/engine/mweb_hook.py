from typing import Type, TypeVar, cast

from mweb.saas.mweb_saas_connector import MWebTenantResolver, MWebExternalSaaSConfig

T = TypeVar('T')


class MWebHook:
    TENANT_RESOLVER: MWebTenantResolver = None
    EXTERNAL_SAAS_CONFIG: MWebExternalSaaSConfig = None

    @classmethod
    def get_hook(cls, hook_name: str, hook_type: Type[T], default=None) -> T | None:
        if hasattr(cls, hook_name):
            hook = getattr(cls, hook_name)
            if hook is None and isinstance(default, hook_type):
                return cast(T, getattr(cls, hook_name))
        return default

    @classmethod
    def external_saas_config(cls) -> MWebExternalSaaSConfig | None:
        return cls.get_hook('EXTERNAL_SAAS_CONFIG', MWebExternalSaaSConfig)

    @classmethod
    def tenant_resolver(cls) -> MWebTenantResolver | None:
        return cls.get_hook('TENANT_RESOLVER', MWebTenantResolver)
