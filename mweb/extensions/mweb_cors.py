import fnmatch
from mweb import MWebBase, MWebConfig, Response, request


class MWebCORS:
    _config: MWebConfig = None

    def register(self, mweb_app: MWebBase, config: MWebConfig):
        self._config = config
        if not config.CORS_ENABLED:
            return
        mweb_app.before_request_funcs.setdefault(None, []).append(self.handle_options)
        mweb_app.after_request_funcs.setdefault(None, []).append(self.add_headers)

    def add_cors_headers(self, response: Response):
        response.headers["Access-Control-Allow-Origin"] = self._config.CORS_ALLOW_ACCESS_CONTROL_ORIGIN
        response.headers["Access-Control-Allow-Methods"] = self._config.CORS_ALLOW_METHODS
        response.headers["Access-Control-Allow-Headers"] = self._config.CORS_ALLOW_HEADERS
        response.headers["Access-Control-Allow-Credentials"] = self._config.CORS_ALLOW_CREDENTIALS
        return response

    def is_cors_path(self, path: str):
        patterns = self._config.CORS_REST_URL_START_WITH + self._config.CORS_STATIC_URL_START_WITH
        return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

    async def handle_options(self):
        if request.method == "OPTIONS" and self.is_cors_path(request.path):
            resp = Response()
            return self.add_cors_headers(resp)
        return None

    async def add_headers(self, response: Response):
        if self.is_cors_path(request.path):
            self.add_cors_headers(response)
        return response
