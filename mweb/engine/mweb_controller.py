from quart import Blueprint


class BaseController(Blueprint):
    pass

class Controller(BaseController):
    def __init__(self, name: str, url: str):
        super().__init__(
            name=name,
            import_name=__name__,
            url_prefix=url
        )


class SSRController(BaseController):

    def __init__(self, name: str, url: str | None = None, package_name: str | None = None, assets_dir: str | None = None, assets_url: str | None = None, template_dir: str | None = None):
        if not package_name:
            package_name = __name__
        super().__init__(
            name=name,
            import_name=package_name,
            url_prefix=url,
            static_folder=assets_dir,
            static_url_path=assets_url,
            template_folder=template_dir,
        )
