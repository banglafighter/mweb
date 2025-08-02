import traceback
from mw_common.mw_console_log import Console
from mw_common.mw_exception import MwException
from mw_common.pw_util import MwUtil
from mweb import MWebSystemConfig
from mweb.engine.mweb_base import MWebBase
from mweb.engine.mweb_config import MWebConfig
from mweb.engine.mweb_connector import MWebAppDefinition, MWebModule
from mweb.engine.mweb_data import MWebModuleDetails
from mweb.engine.mweb_hook import MWebHook
from mweb.engine.mweb_registry import MWebRegistry
from mweb.engine.mweb_util import MWebUtil


class MWebModuleRegistry:
    _mweb_app: MWebBase
    _config: MWebConfig = None
    _mweb_orm = None
    _hook: MWebHook = None
    _system_config: MWebSystemConfig = None

    async def register(self, mweb_app: MWebBase, config: MWebConfig, mweb_orm, hook: MWebHook, system_config: MWebSystemConfig, is_cli: bool = False):
        self._mweb_app = mweb_app
        self._config = config
        self._mweb_orm = mweb_orm
        self._system_config = system_config

        if not hook is None:
            hook = MWebUtil.get_mweb_hooks(config=self._config)

        self._hook = hook
        await self.register_modules(config=config, is_cli=is_cli)

    async def register_modules(self, config: MWebConfig = None, is_cli: bool = False):
        modules = self.get_modules(config=config)
        if not modules or len(modules) == 0 or self._mweb_app is None:
            return

        async with self._mweb_app.app_context():
            for module in modules:
                try:
                    _module: MWebModule = self.validate_and_get_module_instance(module=module)
                    if is_cli:
                        await _module.run_on_cli_init(mweb_app=self._mweb_app, config=self._config)
                    else:
                        self.register_module(module=_module)
                        await _module.initialize(mweb_app=self._mweb_app, config=config, hook=self._hook, system_config=self._system_config)
                        _module.register_model(mweb_orm=self._mweb_orm)
                        _module.register_controller(mweb_app=self._mweb_app)
                        await _module.run_on_start(mweb_app=self._mweb_app, config=self._config)
                except MwException as e:
                    traceback.print_exc()
                    Console.error(e, system_log=True)

    def register_module(self, module: MWebModule):
        details: MWebModuleDetails = module.register_module()
        if not details or not details.systemName:
            raise MwException(f"Please provide module details for {self.get_module_class_name(module=module)}")
        if details.systemName in MWebRegistry.registerModules:
            Console.error(f"{details.systemName} is already registered. Overwriting", system_log=True)
        MWebRegistry.registerModules[details.systemName] = details

    def validate_and_get_module_instance(self, module):
        if not issubclass(module, MWebModule):
            raise MwException(f"Invalid Model {self.get_module_class_name(module)}. Please use a subclass of MWebModule.")
        return module()

    def get_module_class_name(self, module):
        return module.__class__.__name__

    def get_modules(self, config: MWebConfig = None) -> list:
        app_definition = self.get_app_def(config=config)
        if app_definition:
            return app_definition.register_modules()
        return []

    def get_app_def(self, config: MWebConfig = None) -> MWebAppDefinition | None:
        if not config:
            config = self._config
        app_definition = MwUtil.import_from_string(config.APPLICATION_DEFINITION, config.STRING_IMPORT_SILENT)
        if app_definition:
            if not issubclass(app_definition, MWebAppDefinition):
                raise MwException("AppDef must implement MWebAppDefinition")
            return app_definition()
        return None
