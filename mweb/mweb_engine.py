from mweb.engine.mweb_bismillah import MWebBismillah


class MWebEngine(MWebBismillah):
    version = '0.0.1'

    def __init__(self, name, project_root_path, **kwargs):
        self._project_name = name
        super().__init__(name=name, project_root_path=project_root_path, *kwargs)

    @staticmethod
    def bstart(name, project_root_path, **kwargs):
        return MWebEngine(name=name, project_root_path=project_root_path, **kwargs)
