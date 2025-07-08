from quart.cli import QuartGroup, AppGroup


class MWebCLIGroup(QuartGroup):
    pass


class MWebCLI(AppGroup):

    def __init__(self, name: str, help_text: str = None, **kwargs):
        super().__init__(name=name, help=help_text, **kwargs)
