from mweb.engine.mweb_config import MWebConfig


class MWebHelper:

    def set_app_conf_to_conf_res_path(self, app_conf: MWebConfig, conf: MWebConfig):
        # For Resource giving priority to the application configuration, so that a developer can change it via app config
        if app_conf.BASE_DIR is not None:
            conf.BASE_DIR = app_conf.BASE_DIR
        if app_conf.APP_CONFIG_PATH is not None:
            conf.APP_CONFIG_PATH = app_conf.APP_CONFIG_PATH
        if app_conf.TEMP_DIR is not None:
            conf.TEMP_DIR = app_conf.TEMP_DIR
        if app_conf.INTERNAL_DATA_DIR is not None:
            conf.INTERNAL_DATA_DIR = app_conf.INTERNAL_DATA_DIR
        if app_conf.UPLOADED_STATIC_RESOURCES is not None:
            conf.UPLOADED_STATIC_RESOURCES = app_conf.UPLOADED_STATIC_RESOURCES
        if app_conf.UPLOADED_STATIC_RESOURCES_URL is not None:
            conf.UPLOADED_STATIC_RESOURCES_URL = app_conf.UPLOADED_STATIC_RESOURCES_URL
        return conf
