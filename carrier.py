from pypetting import GridSite, Labware
from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    labware: Labware
    position: GridSite


class Carrier:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid

    def site(self, site):
        return GridSite(grid=self.grid, carrier=self.name, site=site)

    def device(self, labware, site):
        gridsite = GridSite(grid=self.grid, carrier=self.name, site=site)
        return Device(labware=labware, position=gridsite)
