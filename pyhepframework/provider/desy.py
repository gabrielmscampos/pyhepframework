import os

from .provider import DatasetProvider


class DESY(DatasetProvider):
    def __init__(self) -> None:
        self.base_path = "/pnfs/desy.de/cms/tier2"

    def resolve_path(self, file_path: str) -> str:
        """
        Resolve prefix to access dataset depending on env
        """
        if file_path.startswith(self.base_path):
            return file_path
        if file_path.startswith("/"):
            file_path = file_path[1:]
        return os.path.join(self.base_path, file_path)
