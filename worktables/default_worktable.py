from pypetting_extra import PintoolDryer, PintoolSetup, Robot, Carrier, Pickolo
from pypetting import Labware, GridSite

robot = Robot()

# carrier
robot.add_carrier("MP 2Pos Fixed", 33)
robot.add_carrier("MP 3Pos Fixed", 40)
robot.add_carrier("MP 3Pos Deck", 22)
robot.add_carrier("Shelf 8x4Pos", 14)
robot.add_carrier("Pintool washstation", 1)
robot.add_carrier("MCA96 Diti 4Pos", 8)
robot.add_carrier("MCA96 3Pos", 15)

# add devices
robot.add_incubator(GridSite(grid=68, site=0, carrier="StoreX 22Pos"))
robot.add_plate_reader(GridSite(grid=51, site=0, carrier="Infinite 200"))

# pickolo setup
light_table = Carrier("Pickolo-Light-Table", 46)
pickolo = Pickolo(
    light_table, "C:\\pickolo\\bin\\PickoloClient.exe", "pypetting_inwell.prf")
robot.add_pickolo(pickolo)

# pintool setup
pin_bleach = robot.carrier["Pintool washstation"].device(
    Labware("Refill Trough MCA96 frt", 16, 24), 3)
pin_water = robot.carrier["Pintool washstation"].device(
    Labware("Refill Trough MCA96 mid", 16, 24), 2)
pin_ethanol = robot.carrier["Pintool washstation"].device(
    Labware("Refill Trough MCA96 bck", 16, 24), 1)
pin_papes_1 = robot.carrier["MCA96 Diti 4Pos"].device(
    Labware("BlottingStation", 16, 24), 3)
pin_papes_2 = robot.carrier["MCA96 Diti 4Pos"].device(
    Labware("BlottingStation", 16, 24), 2)
pin_papes_3 = robot.carrier["MCA96 Diti 4Pos"].device(
    Labware("BlottingStation", 16, 24), 1)
pintool = robot.carrier["MCA96 3Pos"].device(
    site=0, labware=Labware("Pintool", 16, 24))
pin_dryer = PintoolDryer(robot.carrier["Pintool washstation"].site(0), Labware(
    "Pin Tool Dryer", 16, 24, spacing=1))
pintool_setup = PintoolSetup(pintool)
pintool_setup.add_bleach(pin_bleach, pin_papes_1)
pintool_setup.add_water(pin_water, pin_papes_2)
pintool_setup.add_ethanol(pin_ethanol, pin_papes_3)
pintool_setup.add_dryer(pin_dryer)

robot.add_pintool_setup(pintool_setup)
