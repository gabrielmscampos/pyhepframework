from typing import Union, Dict

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

    def start(self):
        """
        Start event loop
        """
        dataset = self.provider.read_file(
            self.provider.resolve_path() + self.config.get("file_path")
        )
        events = self.provider.parse_events(dataset, objects=self.config.get("objects"))

        print("Number of events considered: ", len(events))

        self.evt_handler.set_config(self.config)

        if HAS_TQDM:
            iter_obj = tqdm.tqdm(events)
        else:
            iter_obj = events

        for event in iter_obj:
            self.evt_handler.main(event)
