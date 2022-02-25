from abc import ABC, abstractmethod
from typing import Dict


class EventHandler(ABC):
    @abstractmethod
    def main(self, event: Dict) -> None:
        """
        Main method to make analysis
        """
        ...

    def set_config(self, config) -> None:
        """
        Set analysis parameters in EventHandler object
        """
        self.config = config
