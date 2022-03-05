from .provider import DatasetProvider


class LocalProvider(DatasetProvider):
    def __init__(self) -> None:
        pass

    def resolve_path(self, file_path: str) -> str:
        """
        Resolve prefix to access dataset depending on env
        """
        return file_path
