from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

import uproot
from awkward.highlevel import Array


class DatasetProvider(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def resolve_path(self, file_path: str) -> str:
        """
        Resolve prefix to access dataset depending on env
        """
        ...

    def read_file(self, file_path: str) -> uproot.reading.ReadOnlyDirectory:
        """
        Read chunk from filepath
        """
        file_path = self.resolve_path(file_path)
        return uproot.open(file_path)

    @staticmethod
    def parse_events(
        dataset: uproot.reading.ReadOnlyDirectory, objects: List[str]
    ) -> Tuple[Array, int]:
        """
        Parse events into Array
        """
        events = dataset.get("Events;1")
        entries = events.num_entries
        return events.arrays(objects), entries
