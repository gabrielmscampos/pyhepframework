# pyhepframework

Framework developed from the scratch as an object of study for data analysis at CMS using Python.

# Dependencies

* Python ^3.8

# How to use?

The purpose of this guide is to explain the minimal setup to use `pyhepframework`.

First you need to make sure that you environment contains Python 3.8 (in LXPLUS and DESY naf-cms you can load the LCG_100 environemnt) then you create a virtual environmental and install `pyhepframework` from git.

The following example can be run at DESY naf-cms:

```bash
cd && cd private
source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/setup.sh
mkdir my_analysis && cd my_analysis
python -m venv python_modules
source python_modules/bin/activate
pip install git+https://github.com/gabrielmscampos/pyhepframework
```

The minimal setup is done, `pyhepframework` is built under the dependency injection philosophy it gives complete flexiblity to create your own EventHandler class and plug into the EventLoop.

Create `my_analysis.py` under the `my_analysis` directory and paste the following python analysis code. The purpose of this code is to read and specify file NANOAOD root file, select just a few objects and run the code written under the `main` method.

```python
from typing import Dict, Tuple, List

import numpy as np

from pyhepframework.provider.desy import DESY
from pyhepframework.evt_handler import EventHandler
from pyhepframework.evt_loop import EventLoop

config = {
    "file_path": "store/mc/RunIISummer20UL17NanoAODv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/230000/B5804595-A8F6-DD46-A224-7C115AD91EAA.root",
    "objects": [
        "nJet",
        "Jet_jetId",
        "Jet_pt",
        "Jet_eta",
    ],
}

class MyHandler(EventHandler):
    def main(self, event):
        """
        Main method for analysis
        """
        selected_jets, n_jets = self.select_jets(event)
        print(selected_jets, n_jets)

    def select_jets(self, event: Dict) -> Tuple[List, int]:
        """
        Select jets
        """
        selected_jets = []
        n_jets = 0

        for ijet in range(event.get("nJet")):

            if event.get("Jet_pt")[ijet] <= 20:
                continue
            if event.get("Jet_jetId")[ijet] < 6:
                continue
            if np.abs(event.get("Jet_eta")[ijet]) >= 2.4:
                continue

            n_jets += 1
            selected_jets.append(ijet)

        return selected_jets, n_jets

if __name__ == "__main__":
    provider = DESY()
    evt_handler = MyHandler()
    evt_loop = EventLoop(config, provider, evt_handler)
    evt_loop.start()

```

You can execute this analysis executing:

```
python my_analysis.py
```
