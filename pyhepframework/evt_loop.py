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

    def start(self) -> None:
        """
        Start event loop
        """
        dataset = self.provider.read_file(self.config.get("file_path"))
        events, _ = self.provider.parse_events(dataset, objects=self.config.get("objects"))
        self.evt_handler.set_config(self.config)

        if HAS_TQDM:
            events = tqdm.tqdm(events)

        for event in events:
            # Parsing <Record ...> as Dict[] is much more performatic to the Event Loop
            event = {k: event.__getattr__(k) for k in self.config.get("objects")}
            obj = self.evt_handler.main(event)
            self.__output.append(obj)

    def result(self) -> List:
        """
        Get result from event loop
        """
        return self.__output
