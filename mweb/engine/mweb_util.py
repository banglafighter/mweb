import os
from mw_common.mw_console_log import Console
from mw_common.pw_util import MwUtil
from mweb import MWebSystemConfig
from mweb.engine.mweb_config import MWebConfig
from mweb.engine.mweb_hook import MWebHook


class MWebUtil:

    @staticmethod
    def get_yml_environment_file_name():
        environment_name = os.environ.get('env')
        file_name = "env"
        if environment_name:
            file_name = f"{file_name}-{environment_name}"
        Console.info(f"Environment name: {file_name}", system_log=True)
        return f"{file_name}.yml"

    @staticmethod
    def get_mweb_hooks(config: MWebConfig) -> MWebHook:
        mweb_hook = MWebHook()
        hook_class = MwUtil.import_from_string(config.APPLICATION_HOOK, True)
        if hook_class:
            MwUtil.is_sub_class_of(hook_class, parent_class=MWebHook, message=f"App Hook is not a subclass of MWebHook. Path: {config.APPLICATION_HOOK}")
            hook_map = dir(hook_class)
            for key in hook_map:
                if key.isupper():
                    setattr(mweb_hook, key, getattr(hook_class, key))
        return mweb_hook

    @staticmethod
    def get_mweb_sys_config(config: MWebConfig) -> MWebSystemConfig:
        system_config = MWebSystemConfig()
        system_config_class = MwUtil.import_from_string(config.SYSTEM_CONFIGURATION, True)
        if system_config_class:
            MwUtil.is_sub_class_of(system_config_class, parent_class=MWebSystemConfig, message=f"System Config is not a subclass of MWebSystemConfig. Path: {config.SYSTEM_CONFIGURATION}")
            hook_map = dir(system_config_class)
            for key in hook_map:
                if key.isupper():
                    setattr(system_config, key, getattr(system_config_class, key))
        return system_config

    @staticmethod
    def copy_config_property(source, destination):
        if source and destination:
            config_map = dir(source)
            for key in config_map:
                if key.isupper() and hasattr(destination, key):
                    setattr(destination, key, getattr(source, key))
        return destination
