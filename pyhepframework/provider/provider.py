import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

import uproot3


class DatasetProvider(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def resolve_path(self) -> str:
        """
        Resolve prefix to access dataset depending on env
        """
        ...

    def read_file(self, file_path: str) -> uproot3.rootio.ROOTDirectory:
        """
        Read chunk from filepath
        """
        file_path = os.path.join(self.resolve_path(), file_path)
        return uproot3.open(file_path)

    @staticmethod
    def parse_events(
        dataset: uproot3.rootio.ROOTDirectory, objects: Optional[List]
    ) -> List[Dict]:
        """
        Parse events into List[Dict]
        """
        events = dataset.get("Events;1")
        size = events.get("run").array().size

        if objects is None:
            objects = events.keys()
            objects = [object.decode("utf-8") for object in objects]

        result = [{k: None for k in objects} for _ in range(size)]

        for object in objects:
            values = events.get(object).array()
            for idx, value in enumerate(values):
                result[idx][object] = value

        return result
