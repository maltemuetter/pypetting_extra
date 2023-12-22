from .carrier import Device
from .base import direct_command


class PintoolSetup:
    def __init__(self, pintool: Device):
        self.pintool = pintool
        self.dryer = False

    def add_ethanol(self, trough, blot):
        self.ethanol_trough = trough
        self.ethanol_blot = blot

    def add_water(self, trough, blot):
        self.water_trough = trough
        self.water_blot = blot

    def add_bleach(self, trough, blot):
        self.bleach_trough = trough
        self.bleach_blot = blot

    def add_dryer(self, dryer: Device):
        self.dryer = dryer


def add_wash_step(self, wash_trough: Device, blot: Device):
    self.wash_steps.append(wash_trough)
    self.blot_steps.append(blot)


class PintoolDryer:
    def __init__(self, gridSite, labware, dt=60, timer=11):
        self.gridsite = gridSite
        self.time = dt
        self.timer = timer
        self.labware = labware

    def start_dryer(self):
        return direct_command('Command("O1SLO3,1",1,1,,,2,2,0);')

    def stop_dryer(self):
        return direct_command('Command("O1SLO3,0",1,1,,,2,2,0);')
