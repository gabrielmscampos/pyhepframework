from .provider import DatasetProvider


class CERN(DatasetProvider):
    def __init__(self) -> None:
        pass

    def resolve_path(self) -> str:
        """
        Resolve prefix to access dataset depending on env
        """
        return "root://"
