from pypetting import (
    mca_aspirate,
    mca_dispense,
    start_timer,
    wait_timer,
    mca_drop_tips,
    mca_get_tips,
)
from pypetting.mca import _mca_well_select
from itertools import product


class MCA:
    def __init__(self, tips=[], timer=10, extra_vol=10, liquid_class="Minimal FD"):
        self.tips = tips
        self.tips_mounted = False
        self.pintool_mounted = False
        self.pintool_exists = False
        self.extra_vol = extra_vol
        self.timer = timer
        self.liquid_class = liquid_class

    def add_tips(self, tips: list):
        self.tips.append(tips)

    def add_pintool_setup(self, pintool_setup):
        self.pintool_exists = True
        self.pintool_setup = pintool_setup
        self.pintool = pintool_setup.pintool

    def get_tips(self, tip_idx: int = 0):
        if self.tips_mounted == True:
            raise Exception("tips already mounted")
        self.tips_mounted = True
        self.tip_gridsite = self.tips[tip_idx].gridsite
        wl = mca_get_tips(self.tip_gridsite)
        return wl

    def get_pintool(self):
        if (self.tips_mounted == True) | (self.pintool_mounted == True):
            raise Exception("tips already mounted")
        self.tip_gridsite = self.pintool.gridsite
        self.pintool_mounted = True
        return mca_get_tip_block(self.tip_gridsite, airgap=0)

    def drop_pintool(self):
        if self.pintool_mounted == False:
            raise Exception("tips not mounted")
        self.pintool_mounted = False
        return mca_drop_tip_block(self.tip_gridsite)

    def return_tips(self):
        if self.tips_mounted == False:
            raise Exception("tips not mounted")
        self.tips_mounted = False
        return mca_drop_tips(self.tip_gridsite)

    def aspirate(self, plate, row, col, volume, liquid_class=False, waste=False):
        if not liquid_class:
            liquid_class = self.liquid_class
        if volume > 250:
            raise Exception("MCA cannot aspirate more than 200ul")
        WL = [
            mca_aspirate(
                plate.gridsite,
                row,
                col,
                volume + self.extra_vol * waste,
                liquid_class,
                labware=plate.labware,
            )
        ]
        if waste:
            WL += self.dispense(plate, row, col, self.extra_vol, liquid_class)
        return WL

    def dispense(self, plate, row, col, volume, liquid_class=False):
        if not liquid_class:
            liquid_class = self.liquid_class
        WL = [
            mca_dispense(
                plate.gridsite, row, col, volume, liquid_class, labware=plate.labware
            )
        ]
        return WL

    def mix(self, plate, row, col, volume, cycles, liquid_class=False):
        wl = []
        for _ in range(cycles):
            wl += self.aspirate(plate, row, col, volume, liquid_class=liquid_class)
            wl += self.dispense(plate, row, col, volume, liquid_class=liquid_class)
        return wl

    def replicate_with_pintool(self, source, destination, n=2, dip_speed=30):
        WL = self.dip(source, n=n, dip_speed=dip_speed) + self.dip(
            destination, n=n, dip_speed=dip_speed
        )
        return WL

    def dip(self, plate, n=2, dip_speed=60, wait_time=1):
        wl = [self.move(plate)]
        for _ in range(n - 1):
            wl.append(self.move(plate, z_pos=3, speed=dip_speed, local=4))
            wl.append(start_timer(self.timer))
            wl.append(wait_timer(self.timer, wait_time))
            wl.append(self.move(plate, z_pos=2, speed=dip_speed, local=4))
        wl.append(self.move(plate, z_pos=3, speed=dip_speed, local=4))
        wl.append(self.move(plate, z_pos=2, speed=5, local=4))
        return wl

    def blot(self, pape, dt=2):
        wl = [self.move(pape, z_pos=3)]
        wl.append(start_timer(self.timer))
        wl.append(wait_timer(self.timer, dt))
        return wl

    def dry_pintool(self, dt=60):
        wl = [self.move(self.pintool_setup.dryer)]
        wl.append(start_timer(self.timer))
        wl.append(self.pintool_setup.dryer.start_dryer())
        wl.append(wait_timer(self.timer, dt))
        wl.append(self.pintool_setup.dryer.stop_dryer())
        return wl

    def clean_pintool(self, blot_time=3, dry_time=30):
        setup = self.pintool_setup
        WL = []
        WL += self.dip(setup.bleach_trough)
        WL += self.blot(setup.bleach_blot, blot_time)
        WL += self.dip(setup.water_trough)
        WL += self.blot(setup.water_blot, blot_time)
        WL += self.dip(setup.ethanol_trough)
        WL += self.blot(setup.ethanol_blot, blot_time)
        WL += self.dry_pintool(dt=dry_time)
        return WL

    def move(
        self,
        plate,
        col: int = 1,
        row: int = 1,
        z_pos: int = 0,
        speed: int = 10,
        local: int = 0,
    ):
        labware = plate.labware
        spacing = labware.spacing
        grid_site = plate.gridsite
        command = (
            (
                "B;MCAMove("
                "255,"
                f"{grid_site.grid},"
                f"{grid_site.site},"
                f'{spacing},"'
            ).encode()
            + _mca_well_select(row, col, labware)
            + (f'",{local},{z_pos},0,{speed},0,0);').encode()
        )
        return command

    def fill_96plate(
        self, src, dest, volume, get_tips=True, tip_idx=0, liquid_class=False
    ):
        wl = []
        if get_tips:
            wl.append(self.get_tips(tip_idx=tip_idx))

        wl.extend(self.aspirate(src, 1, 1, volume, liquid_class=liquid_class))
        wl.extend(self.dispense(dest, 1, 1, volume, liquid_class=liquid_class))
        if get_tips:
            wl.append(self.return_tips())
        return wl

    def fill_384plate(
        self, src, dest, volume, tip_idx=0, liquid_class=False, get_tips=True
    ):
        wl = []
        if get_tips and not self.tips_mounted:
            wl.append(self.get_tips(tip_idx=tip_idx))

        for row, col in product([1, 2], [1, 2]):
            wl.extend(self.aspirate(src, row, col, volume, liquid_class=liquid_class))
            wl.extend(self.dispense(dest, row, col, volume, liquid_class=liquid_class))
        if get_tips:
            wl.append(self.return_tips())
        return wl


def mca_get_tip_block(grid_site, airgap: int = 20):
    return f"B;MCAGetTips({grid_site.grid},{grid_site.site},{airgap},0);".encode()


def mca_drop_tip_block(grid_site):
    return f"B;MCADropTips({grid_site.grid},{grid_site.site},1,0);".encode()
