from quart import Blueprint


class Controller(Blueprint):
    _blueprint = Blueprint = None

    def __init__(self, name: str, url: str):
        super().__init__(
            name=name,
            import_name=__name__,
            url_prefix=url
        )
