import os


class MWebConfig:
    APP_NAME: str = "MWeb"
    PORT: int = 4012
    HOST: str = "127.0.0.1"

    DEBUG: bool = True
    SECRET_KEY: str = 'random_secret_key_base'

    ENABLE_AUTH: bool = True
    ENABLE_SAAS: bool = False

    # Database Configuration
    DB_CONNECTION_URI: str = None
    DB_MULTI_CONNECTION_URIS: dict[str, str] = {}
    DB_PRINT_LOG: bool = False
    DB_EXPIRE_ON_COMMIT: bool = False

    DB_FUTURE: bool = True  # Recommended for SQLAlchemy 2.0 style
    DB_POOL_PRE_PING: bool = True  # Check if connections are alive before using them
    DB_POOL_SIZE: int = 5  # Number of concurrent connections to keep in the pool
    DB_MAX_OVERFLOW: int = 10  # Additional connections beyond pool_size (total max 20+30)
    DB_POOL_TIMEOUT: int = 30  # How long (in seconds) to wait for a connection before raising an error
    DB_POOL_RECYCLE: int = -1  # Recycle connections every 30 minutes to avoid stale ones


    # Resource Management
    BASE_DIR: str = None  # Root Directory
    APP_CONFIG_PATH: str = None
    TEMP_DIR: str = None
    INTERNAL_DATA_DIR: str = None
    UPLOADED_STATIC_RESOURCES: str = None
    UPLOADED_STATIC_RESOURCES_URL: str = "/assets"

    STRING_IMPORT_SILENT: bool = False
    APPLICATION_CONFIGURATION: str = "application.config.app_config.Config"
    SYSTEM_CONFIGURATION: str = "application.config.app_sys_config.SystemConfig"
    APPLICATION_HOOK: str = "application.config.app_hook.Hook"
    APPLICATION_DEFINITION: str = "application.config.app_def.AppDef"

    # CORS
    CORS_ENABLED: bool = True
    CORS_REST_URL_START_WITH: list = ["/api/*"]
    CORS_STATIC_URL_START_WITH: list = ["/static/*"]
    CORS_ALLOW_ORIGINS: list = ["*"]
    CORS_ALLOW_ACCESS_CONTROL_ORIGIN: str = "*"
    CORS_ALLOW_METHODS: str = "GET,POST,DELETE,OPTIONS"
    CORS_ALLOW_HEADERS: str = "Authorization,Content-Type"
    CORS_ALLOW_CREDENTIALS: str = "true"

    def set_base_dir(self, path):
        if not self.BASE_DIR:
            self.BASE_DIR = path
            self.APP_CONFIG_PATH = path
            if not self.DB_CONNECTION_URI:
                self.DB_CONNECTION_URI = 'sqlite+aiosqlite:///' + os.path.join(self.BASE_DIR, 'mweb.sqlite3')
            if "MWebSaaS" not in self.DB_MULTI_CONNECTION_URIS:
                self.DB_MULTI_CONNECTION_URIS["MWebSaaS"] = 'sqlite+aiosqlite:///' + os.path.join(self.BASE_DIR, 'mweb-saas.sqlite3')
        if not self.UPLOADED_STATIC_RESOURCES:
            self.UPLOADED_STATIC_RESOURCES = os.path.join(self.BASE_DIR, "uploaded-resources")
        if not self.TEMP_DIR:
            self.TEMP_DIR = os.path.join(self.BASE_DIR, "mweb-temp")
        if not self.INTERNAL_DATA_DIR:
            self.INTERNAL_DATA_DIR = os.path.join(self.BASE_DIR, "mweb-internal")
        return self
