# pypetting_extra

Write protocols for the Tecan Freedom EVO 200 liquid-handling robot in Python.

`pypetting_extra` builds on [pypetting](https://github.com/sirno/pypetting),
which generates worklists (`.gwl`) for the robot. It adds a model of the robot's
worktable and its devices, so an experiment can be described in terms of plates,
positions and actions instead of raw commands.

## What it covers

- **Worktable**: carriers, sites and labware, with a default worktable layout
  (`worktables/default_worktable.py`).
- **Arms and devices**: pipetting arm (`LiHA`), multichannel arm (`MCA`), plate
  robot (`ROMA`), incubator/storage (`StoreX`), plate reader
  (`InfinitePlateReader`), pin tool, plate tilter and colony picker (`Pickolo`).
- **Experiments**: `Experiment` sets up folders, protocols and worklists and
  logs each step with a message.

## Example

```python
from pypetting_extra import Experiment
from pypetting_extra import default_worktable as worktable
from pypetting.labware import labwares

experiment = Experiment("test1", local_path, robot_path)
protocol = experiment.setup_protocol()

shelf = worktable.carrier["Shelf 8x4Pos"]
plate = shelf.define_plate("dilution_plate", labwares["greiner96"], 31, is_store_pos=True)
liha = worktable.liha

wl = experiment.setup_worklist("test_script.gwl", protocol=protocol)
wl.add(liha.aspirate(plate, 1, 10, 8 * [True]))
wl.add(liha.dispense(plate, 2, 10, 8 * [True]), msg="transferred_medium")
```

A full example is in `example/test_main.py`.

## Installation

```bash
git clone https://github.com/maltemuetter/pypetting_extra.git
pip install -r pypetting_extra/requirements.txt
```

Put the folder that contains `pypetting_extra/` on your Python path.

## Context

Written during my PhD at ETH Zurich to run high-throughput antibiotic
experiments on an automated lab platform.

## License

MIT, see `LICENSE.md`.
