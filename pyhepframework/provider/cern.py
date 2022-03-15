from .provider import DatasetProvider


class CERN(DatasetProvider):
    def __init__(self, redirector: str) -> None:
        self.protocol = "root://"  # XRootD
        self.redirector = redirector

    def resolve_path(self, file_path: str) -> str:
        """
        Resolve prefix to access dataset depending on env
        """
        if file_path.startswith("/") is False:
            file_path = "/" + file_path
        return self.protocol + self.redirector + "//" + file_path
