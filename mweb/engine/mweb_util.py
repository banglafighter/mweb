import os
from mw_common.mw_console_log import Console


class MWebUtil:

    @staticmethod
    def get_yml_environment_file_name():
        environment_name = os.environ.get('env')
        file_name = "env"
        if environment_name:
            file_name = f"{file_name}-{environment_name}"
        Console.info(f"Environment name: {file_name}", system_log=True)
        return f"{file_name}.yml"
