import os
from mw_common.mw_console_log import Console
from mw_common.pw_util import MwUtil
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
    def get_mweb_hooks(config: MWebConfig):
        mweb_hook = MWebHook()
        hook_class = MwUtil.import_from_string(config.APPLICATION_HOOK, True)
        if hook_class:
            hook_map = dir(hook_class)
            for key in hook_map:
                if key.isupper():
                    setattr(mweb_hook, key, getattr(hook_class, key))
