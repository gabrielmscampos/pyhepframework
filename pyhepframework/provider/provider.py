from abc import ABC, abstractmethod
from typing import List, Dict, Optional

import uproot


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
        dataset: uproot.reading.ReadOnlyDirectory, objects: Optional[List]
    ) -> List[Dict]:
        """
        Parse events into List[Dict]
        """
        events = dataset.get("Events;1")
        size = len(events.get("run").array())

        if objects is None:
            objects = events.keys()

        result = [{k: None for k in objects} for _ in range(size)]

        for object in objects:
            values = events.get(object).array()
            for idx, value in enumerate(values):
                result[idx][object] = value

        return result
