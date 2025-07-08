from mweb_orm.common.mweb_orm_connector import MWebTenantResolver
from typing import Type, TypeVar, cast

T = TypeVar('T')


class MWebHook:
    TENANT_RESOLVER: MWebTenantResolver = None

    @classmethod
    def get_hook(cls, hook_name: str, hook_type: Type[T], default=None) -> T | None:
        if hasattr(cls, hook_name):
            hook = getattr(cls, hook_name)
            if hook is None and isinstance(default, hook_type):
                return cast(T, getattr(cls, hook_name))
        return default
