from pypetting_extra import PintoolDryer, Carrier, PintoolSetup, Plate
from pypetting import Labware, GridSite
from pypetting.labware import labwares


#  Make Carrier
mp2 = Carrier("MP 2Pos Fixed", 33)
mp3 = Carrier("MP 3Pos Fixed", 40)
mp_3pos_deck = Carrier("MP 3Pos Deck", 22)
shelf = Carrier("Shelf 8x4Pos", 14)
pintool_wash_station = Carrier("Pintool washstation", 1)
mca_4pos = Carrier("MCA96 Diti 4Pos", 8)
mca_3pos = Carrier("MCA96 3Pos", 15)


# Make positions
lid1_pos = mp2.site(0)
lid2_pos = mp2.site(1)
plate1_pos = mp3.site(0)
plate2_pos = mp3.site(1)
dil_pos = mp3.site(2)
storex_site = GridSite(grid=68, site=0, carrier="StoreX 22Pos")
reader_site = GridSite(grid=51, site=0, carrier="Infinite 200")


# Plates
strainplate = Plate(name="strain", start_position=storex_site,
                    labware=labwares["greiner384"], incubating=True, storex_cart=1, cart_site=1)
exponential_plate = Plate(name="assay_1", start_position=storex_site,
                          labware=labwares["greiner384"], incubating=True, storex_cart=1, cart_site=2)
assayplate = Plate(name="assay_1", start_position=storex_site,
                   labware=labwares["greiner384"], incubating=True, storex_cart=1, cart_site=3)
antibiotic_plate = Plate(
    name="antibiotics", start_position=shelf.site(31), labware=labwares["greiner96"])


# Reservoirs
medium_trough = mp_3pos_deck.device(Labware("Trough 300ml MCA96", 8, 12), 0)
h2o_trough = mp_3pos_deck.device(Labware("Trough 300ml MCA96", 8, 12), 2)
strain_reservoir_12col = mp_3pos_deck.device(
    Labware("12Col Through", 8, 12), 1)

# Fixed Labware
ditis_1 = mca_4pos.device(Labware("200ul DiTi", 16, 24), 0)

pin_bleach = pintool_wash_station.device(
    Labware("Refill Trough MCA96 frt", 16, 24), 3)
pin_water = pintool_wash_station.device(
    Labware("Refill Trough MCA96 mid", 16, 24), 2)
pin_ethanol = pintool_wash_station.device(
    Labware("Refill Trough MCA96 bck", 16, 24), 1)
pin_papes_1 = mca_4pos.device(Labware("BlottingStation", 16, 24), 3)
pin_papes_2 = mca_4pos.device(Labware("BlottingStation", 16, 24), 2)
pin_papes_3 = mca_4pos.device(Labware("BlottingStation", 16, 24), 1)


# Pintool setup
pintool = mca_3pos.device(site=0, labware=Labware("Pintool", 16, 24))
pin_dryer = PintoolDryer(pintool_wash_station.site(0), Labware(
    "Pin Tool Dryer", 16, 24, spacing=1))
pintool_setup = PintoolSetup(pintool)
pintool_setup.add_bleach(pin_bleach, pin_papes_1)
pintool_setup.add_water(pin_water, pin_papes_2)
pintool_setup.add_ethanol(pin_ethanol, pin_papes_3)
pintool_setup.add_dryer(pin_dryer)
