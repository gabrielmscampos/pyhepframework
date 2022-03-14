from typing import Dict, Tuple, List

import numpy as np

from pyhepframework.provider.local import LocalProvider
from pyhepframework.evt_handler import EventHandler
from pyhepframework.evt_loop import EventLoop

config = {
    "dataset_year": "2016preVFP",
    "file_path": "./datasets/738A8F4E-59B1-4441-9D99-48A1B3EEC981.root",
    "objects": [
        "nJet",
        "Jet_jetId",
        "Jet_hadronFlavour",
        "Jet_pt",
        "Jet_eta",
        "Jet_btagDeepB",
        "Jet_btagDeepFlavB",
    ],
    "btagging": {"algorithm": "DeepCSV", "working_point": "loose"},
    "base_selection": {"jet_pt": 20, "jet_eta": 2.4, "jet_id": 6},
}

btag_workingpoints = {
    "DeepJet": {
        "2016postVFP": {
            "loose": 0.0480,
            "medium": 0.2489,
            "tight": 0.6377,
        },
        "2016preVFP": {
            "loose": 0.0508,
            "medium": 0.2598,
            "tight": 0.6502,
        },
        "2017": {
            "loose": 0.0532,
            "medium": 0.3040,
            "tight": 0.7476,
        },
        "2018": {
            "loose": 0.0490,
            "medium": 0.2783,
            "tight": 0.7100,
        },
    },
    "DeepCSV": {
        "2016postVFP": {
            "loose": 0.1918,
            "medium": 0.5847,
            "tight": 0.8767,
        },
        "2016preVFP": {
            "loose": 0.2027,
            "medium": 0.6001,
            "tight": 0.8819,
        },
        "2017": {
            "loose": 0.1355,
            "medium": 0.4506,
            "tight": 0.7738,
        },
        "2018": {
            "loose": 0.1208,
            "medium": 0.4168,
            "tight": 0.7665,
        },
    },
}


class MyHandler(EventHandler):
    def main(self, event):
        """
        Main method for analysis
        """
        selected_jets, n_jets, n_bjets = self.select_jets(event)
        leading_bjet, trailing_bjet = self.find_leading_and_trailing_bjets(
            event, selected_jets, self.config.get("btagging").get("algorithm")
        )
        return {
            "n_jets": n_jets,
            "n_bjets": n_bjets,
            "idx_leading_bjet": leading_bjet,
            "idx_trailing_bjet": trailing_bjet
        }

    @staticmethod
    def is_bjet(btag: float, algorithm: str, year: str, working_point: str) -> bool:
        """
        Determine if jet is a b-jet
        """
        return btag > btag_workingpoints.get(algorithm).get(year).get(working_point)

    def select_jets(self, event: Dict):
        """
        Select jets
        """
        selected_jets = []
        n_jets = 0
        n_bjets = 0

        for ijet in range(event.get("nJet")):

            if event.get("Jet_pt")[ijet] <= self.config.get("base_selection").get(
                "jet_pt"
            ):
                continue
            if event.get("Jet_jetId")[ijet] < self.config.get("base_selection").get(
                "jet_id"
            ):
                continue
            if np.abs(event.get("Jet_eta")[ijet]) >= self.config.get(
                "base_selection"
            ).get("jet_eta"):
                continue

            is_bjet = self.is_bjet(
                event.get("Jet_btagDeepB")[ijet],
                self.config.get("btagging").get("algorithm"),
                self.config.get("dataset_year"),
                self.config.get("btagging").get("working_point"),
            )

            n_jets += 1
            n_bjets += 1 if is_bjet else 0
            selected_jets.append(ijet)

        return selected_jets, n_jets, n_bjets

    def find_leading_and_trailing_bjets(
        self, event: Dict, selected_jets: List, algorithm: str
    ) -> Tuple[int, int]:
        """
        Among all b-jets find leading and trailing
        """
        ijet_leading = -1
        ijet_trailing = -1
        leading_btag = -999.0
        trailing_btag = -999.0
        btagging_variable = (
            event.get("Jet_btagDeepB")
            if algorithm == self.config.get("btagging").get("algorithm")
            else event.get("Jet_btagDeepFlavB")
        )

        if len(selected_jets) == 1:
            ijet_leading = selected_jets[0]
            leading_btag = btagging_variable[ijet_leading]
        else:
            for ijet in selected_jets:
                jet_btag = btagging_variable[ijet]
                if jet_btag > leading_btag:
                    trailing_btag = leading_btag
                    ijet_trailing = ijet_leading
                    leading_btag = jet_btag
                    ijet_leading = ijet
                elif jet_btag > trailing_btag:
                    ijet_trailing = ijet
                    trailing_btag = jet_btag

        return ijet_leading, ijet_trailing


if __name__ == "__main__":
    provider = LocalProvider()
    evt_handler = MyHandler()
    evt_loop = EventLoop(config, provider, evt_handler)
    evt_loop.start()
    result = evt_loop.result()
    print(result[0])