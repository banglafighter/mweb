import asyncio
from mw_common import Console
from mweb import MWebBase, MWebConfig, MWebSystemConfig
from mweb.engine.mweb_cli import MWebCLI
from mweb.engine.mweb_hook import MWebHook
from mweb.engine.mweb_module_registry import MWebModuleRegistry

mweb_module_cli = MWebCLI("module", help_text="MWeb Module CLI System")
_mweb_modc_mweb_app: MWebBase | None = None
_mweb_modc_config: MWebConfig | None = None
_mweb_modc_hook: MWebHook | None = None
_mweb_modc_system_config: MWebSystemConfig | None = None
_mweb_modc_mweb_orm = None


@mweb_module_cli.command("init", help="Initialize module CLI init")
def module_init_cli():
    asyncio.run(module_init_cli_async())


async def module_init_cli_async():
    try:
        async with _mweb_modc_mweb_app.app_context():
            module_registry = MWebModuleRegistry()
            await module_registry.register(
                mweb_app=_mweb_modc_mweb_app,
                config=_mweb_modc_config,
                hook=_mweb_modc_hook,
                system_config=_mweb_modc_system_config,
                mweb_orm=_mweb_modc_mweb_orm,
                is_cli=True
            )
    except Exception as e:
        Console.error(str(e))


def register_mweb_module_cli(mweb_app: MWebBase, config: MWebConfig, hook: MWebHook, system_config: MWebSystemConfig, mweb_orm):
    global _mweb_modc_mweb_app
    global _mweb_modc_config
    global _mweb_modc_hook
    global _mweb_modc_system_config
    global _mweb_modc_mweb_orm

    _mweb_modc_mweb_app = mweb_app
    _mweb_modc_config = config
    _mweb_modc_hook = hook
    _mweb_modc_system_config = system_config
    _mweb_modc_mweb_orm = mweb_orm
    if mweb_app is not None:
        mweb_app.cli.add_command(mweb_module_cli)
