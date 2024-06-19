from pypetting_extra import (
    PintoolDryer,
    PintoolSetup,
    Worktable,
    Carrier,
    Pickolo,
    PlateTilter,
)
from pypetting import Labware, GridSite


worktable = Worktable()

# carrier
worktable.add_carrier("MP 2Pos Fixed", 33, 2)
worktable.add_carrier("MP 3Pos Fixed", 40, 3)
worktable.add_carrier("MP 3Pos Deck", 22, 3)
worktable.add_carrier("Shelf 8x4Pos", 14, 32)
worktable.add_carrier("Pintool washstation", 1, 4)
worktable.add_carrier("MCA96 Diti 4Pos", 8, 4)
worktable.add_carrier("MCA96 3Pos", 15, 3)

# add devices
worktable.add_incubator(GridSite(grid=68, site=0, carrier="StoreX 22Pos"))
worktable.add_plate_reader(GridSite(grid=51, site=0, carrier="Infinite 200"))
tilter = PlateTilter("1Pos Tilter", 62)
worktable.add_tilter(tilter)

# Tips
tips = worktable.carrier["MCA96 Diti 4Pos"].define_labware(
    Labware("DiTi 200ul SBS MCA96", 8, 12), 0
)
worktable.add_tips(tips)

# pickolo setup
light_table = Carrier("Pickolo-Light-Table", 46, 2)
pickolo = Pickolo(
    light_table, "C:\\pickolo\\bin\\PickoloClient.exe", "pypetting_inwell.prf"
)
worktable.add_pickolo(pickolo)

# pintool setup
pin_bleach = worktable.carrier["Pintool washstation"].define_labware(
    Labware("Refill Trough MCA96 frt", 16, 24), 3
)
pin_water = worktable.carrier["Pintool washstation"].define_labware(
    Labware("Refill Trough MCA96 mid", 16, 24), 2
)
pin_ethanol = worktable.carrier["Pintool washstation"].define_labware(
    Labware("Refill Trough MCA96 bck", 16, 24), 1
)
pin_papes_1 = worktable.carrier["MCA96 Diti 4Pos"].define_labware(
    Labware("BlottingStation", 16, 24), 3
)
pin_papes_2 = worktable.carrier["MCA96 Diti 4Pos"].define_labware(
    Labware("BlottingStation", 16, 24), 2
)
pin_papes_3 = worktable.carrier["MCA96 Diti 4Pos"].define_labware(
    Labware("BlottingStation", 16, 24), 1
)
pintool = worktable.carrier["MCA96 3Pos"].define_labware(
    site=0, labware=Labware("Pintool", 16, 24)
)
pin_dryer = PintoolDryer(
    worktable.carrier["Pintool washstation"].gridsite(0),
    Labware("Pin Tool Dryer", 16, 24, spacing=1),
)
pintool_setup = PintoolSetup(pintool)
pintool_setup.add_bleach(pin_bleach, pin_papes_1)
pintool_setup.add_water(pin_water, pin_papes_2)
pintool_setup.add_ethanol(pin_ethanol, pin_papes_3)
pintool_setup.add_dryer(pin_dryer)

worktable.add_pintool_setup(pintool_setup)
