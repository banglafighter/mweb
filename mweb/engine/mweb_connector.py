from abc import ABC, abstractmethod
from mweb.engine.mweb_system_config import MWebSystemConfig
from mweb.engine.mweb_base import MWebBase
from mweb.engine.mweb_config import MWebConfig
from mweb.engine.mweb_data import MWebModuleDetails
from mweb.engine.mweb_hook import MWebHook


class MWebAppDefinition(ABC):
    @abstractmethod
    def register_modules(self) -> list:
        """
        Register the modules which want to add into the application.
        :return:
        """
        return []


class MWebModule(ABC):
    """
    Responsibility: Register and Initialize MWeb Modules
    Method Calling Precedence:
    1. register_module
    2. initialize
    3. register_model
    4. register_controller
    5. conditionals
    ... run_on_start
    ... run_on_cli_init
    """

    @abstractmethod
    def register_module(self) -> MWebModuleDetails:
        """
        Precedence: 1
        Every module needs to be registered by passing their information.
        """

    @abstractmethod
    async def initialize(self, mweb_app: MWebBase, config: MWebConfig, hook: MWebHook, system_config: MWebSystemConfig, **kwargs):
        """
        Precedence: 2
        """

    @abstractmethod
    def register_model(self, mweb_orm) -> list:
        """
        Precedence: 3
        Normally Models are automatically register if not registered, then pass here
        """

    @abstractmethod
    def register_controller(self, mweb_app: MWebBase):
        """
        Precedence: 4
        Register all the controllers of the module
        """

    @abstractmethod
    async def run_on_start(self, mweb_app: MWebBase, config: MWebConfig):
        """
        Precedence: 5
        It will call when the application is started.
        """

    @abstractmethod
    async def run_on_cli_init(self, mweb_app: MWebBase, config: MWebConfig):
        """
        Precedence: 6
        Only call when `module init` command run from cli
        """
