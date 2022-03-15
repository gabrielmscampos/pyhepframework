from typing import Union, Dict, List

from injector import inject

from .provider import cern, desy, local
from .evt_handler import EventHandler

try:
    import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


class EventLoop:
    @inject
    def __init__(
        self,
        config: Dict,
        provider: Union[cern.CERN, desy.DESY, local.LocalProvider],
        evthandler: EventHandler,
    ) -> None:
        self.provider = provider
        self.evt_handler = evthandler
        self.config = config
        self.__output = []

    @staticmethod
    def __validate_max_entries(max_events):
        """
        Validate max events configuration
        """
        if max_events is None:
            return -1
        if isinstance(max_events, (int, str)) is False:
            raise ValueError(
                "Max events must be a valid integer (or str-representation)."
            )
        if max_events < -1 or max_events == 0:
            raise ValueError(
                "Max events must be -1 (consider all events) or higher than 0."
            )
        return int(max_events)

    @staticmethod
    def __resolve_considered_events(max_events, n_events):
        """
        Resolve number of events considered in event loop
        """
        if max_events == -1 or max_events > n_events:
            return n_events
        return max_events

    def start(self) -> None:
        """
        Start event loop
        """
        self.evt_handler.set_config(self.config)
        max_events = self.__validate_max_entries(self.config.get("max_events"))

        dataset = self.provider.read_file(self.config.get("file_path"))
        events, n_events = self.provider.parse_events(
            dataset, objects=self.config.get("objects")
        )
        considered_events = self.__resolve_considered_events(max_events, n_events)

        if HAS_TQDM:
            events = tqdm.tqdm(events, total=considered_events)

        for evt_number, event in enumerate(events, start=1):

            # Control number of considered events chosen by user
            if evt_number > considered_events:
                break

            # Parsing <Record ...> as Dict[] is much more performatic to the Event Loop
            event = {k: event.__getattr__(k) for k in self.config.get("objects")}
            obj = self.evt_handler.main(event)
            self.__output.append(obj)

    def result(self) -> List:
        """
        Get result from event loop
        """
        return self.__output
