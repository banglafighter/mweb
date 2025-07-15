import contextvars
from .mweb_saas_connector import MWebTenantResolver


class MWebSaaSConst:
    TENANT_KEY = "tkey"


tenant_key_context_var = contextvars.ContextVar("mweb_saas_tenant_key", default=None)


class MWebSaaS:

    @classmethod
    def init_tenant_key(cls, tenant_key=None):
        from ..engine.mweb_hook import MWebHook
        try:
            tenant_resolver: MWebTenantResolver = MWebHook.tenant_resolver()
            if tenant_key:
                return tenant_key
            elif tenant_resolver:
                tenant_key = tenant_resolver.get_tenant_key()

            if tenant_key:
                cls.set_tenant_key(tenant_key)
        except Exception as e:
            raise e
        except:
            pass
        return tenant_key

    @classmethod
    def set_tenant_key(cls, key: str):
        tenant_key_context_var.set(key)

    @classmethod
    def get_tenant_key(cls):
        tenant_key = tenant_key_context_var.get()
        return cls.init_tenant_key(tenant_key=tenant_key)
