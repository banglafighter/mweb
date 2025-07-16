import os
import click
import asyncio
from mw_common.mw_console_log import Console
from mw_common.mw_data_util import DataUtil
from mw_common.pw_util import MwUtil
from mw_file_content.file.mwfc_file_util import FileUtil
from mw_file_content.file_content.mwfc_data_file_util import DataFileUtil
from mweb.engine.mweb_base import MWebBase
from mweb.engine.mweb_cli import MWebCLIGroup
from mweb.engine.mweb_config import MWebConfig
from mweb.engine.mweb_data import MWebInternalConfig
from mweb.engine.mweb_helper import MWebHelper
from mweb.engine.mweb_hook import MWebHook
from .mweb_system_config import MWebSystemConfig
from mweb.engine.mweb_module_registry import MWebModuleRegistry
from mweb.engine.mweb_registry import MWebRegistry
from mweb.engine.mweb_util import MWebUtil
from mweb_auth.mweb_auth_module import MWebAuthModule
from mweb_crud import MWebCRUDModule
from mweb_orm.mweb_orm_module import MWebORMModule
from mweb_orm.orm.mweb_orm import mweb_orm
from ..cli.mweb_module_cli import register_mweb_module_cli
from ..extensions.mweb_cors import MWebCORS


class MWebBismillah:
    _mweb_app: MWebBase = None
    _config: MWebConfig = None
    _mweb_helper: MWebHelper = None
    _mweb_module_registry: MWebModuleRegistry = None
    _hook: MWebHook = None
    _system_config: MWebSystemConfig = None

    def __init__(self, project_root_path: str, name: str = "MWeb", config: MWebConfig = None, internal_config: MWebInternalConfig = None):
        self._mweb_helper = MWebHelper()
        if not internal_config:
            internal_config = MWebInternalConfig()

        self._mweb_app = MWebBase(
            import_name=name,
            static_url_path=internal_config.staticUrlPath,
            static_folder=internal_config.staticFolder,
            static_host=internal_config.staticHost,
            host_matching=internal_config.hostMatching,
            subdomain_matching=internal_config.subdomainMatching,
            template_folder=internal_config.templateFolder,
            instance_path=internal_config.instancePath,
            instance_relative_config=internal_config.instanceRelativeConfig,
            root_path=internal_config.rootPath,
        )

        # Initialization
        self._merge_config(project_root_path=project_root_path, provided_config=config)
        MWebRegistry.mweb_app = self._mweb_app
        self._hook = MWebUtil.get_mweb_hooks(config=self._config)
        self._system_config = MWebUtil.get_mweb_sys_config(config=self._config)

        # Register System Module
        self._register_system_modules()

        # Register CLI
        self._register_cli()
        self._register_extensions()

        # Register Module
        self._mweb_module_registry = MWebModuleRegistry()
        asyncio.run(
            self._mweb_module_registry.register(
                mweb_app=self._mweb_app,
                config=self._config,
                hook=self._hook,
                mweb_orm=mweb_orm,
                system_config=self._system_config,
                is_cli=False
            )
        )

    def run(self):
        self._mweb_app.run(host=self._config.HOST, port=self._config.PORT, debug=self._config.DEBUG)

    def get_app(self):
        return self._mweb_app

    def cli(self):
        Console.yellow("----------------------------------------", system_log=True)
        Console.green("         Welcome to MWeb CLI   ", True, system_log=True)
        Console.yellow("----------------------------------------", system_log=True)

        @click.group(cls=MWebCLIGroup, create_app=self.get_app)
        def invoke_cli_script():
            pass

        return invoke_cli_script()

    def _merge_config(self, project_root_path: str, provided_config: MWebConfig):
        if not provided_config:
            provided_config = MWebConfig()

        app_config_class = MwUtil.import_from_string(provided_config.APPLICATION_CONFIGURATION, False)
        MwUtil.is_sub_class_of(app_config_class, parent_class=MWebConfig, message=f"App Config is not a subclass of MWebConfig. Path: {provided_config.APPLICATION_CONFIGURATION}")
        provided_config = self._mweb_helper.set_app_conf_to_conf_res_path(app_conf=app_config_class, conf=provided_config)

        # Set Resource Path
        root_dir = os.path.dirname(os.path.abspath(project_root_path))
        provided_config.set_base_dir(root_dir)

        # Merge all the application config into provided config
        app_config_props = app_config_class.__dict__
        for conf_property_key, conf_property_value in app_config_props.items():
            if conf_property_key.isupper() and not callable(conf_property_value) and not conf_property_key.startswith("__") and hasattr(provided_config, conf_property_key):
                setattr(provided_config, conf_property_key, getattr(app_config_class, conf_property_key))

        # Read YAML Configuration and Update to Application Config
        yml_config_file = FileUtil.join_path(provided_config.APP_CONFIG_PATH, MWebUtil.get_yml_environment_file_name())
        yml_config_dict = DataFileUtil.read_yaml(file_path=yml_config_file, raise_exception=False)
        if yml_config_dict:
            for yaml_property in yml_config_dict:
                value = DataUtil.dict_value(yml_config_dict, yaml_property)
                setattr(app_config_class, yaml_property, value)
                setattr(provided_config, yaml_property, value)


        self._config = provided_config
        MWebRegistry.config = provided_config

    def _register_system_modules(self):
        MWebORMModule().register(mweb_app=self._mweb_app, config=self._config, hook=self._hook)
        MWebCRUDModule().register(mweb_app=self._mweb_app, config=self._config, hook=self._hook)

        if self._config.ENABLE_AUTH:
            MWebAuthModule().register(mweb_app=self._mweb_app, config=self._config, hook=self._hook, system_config=self._system_config)

    def _register_cli(self):
        register_mweb_module_cli(mweb_app=self._mweb_app, config=self._config, hook=self._hook, system_config=self._system_config, mweb_orm=mweb_orm)

    def _register_extensions(self):
        MWebCORS().register(mweb_app=self._mweb_app, config=self._config)
