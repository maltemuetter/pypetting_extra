from default_worktable import robot
from pypetting_extra import  Plate
from pypetting import Labware, GridSite
from pypetting.labware import labwares


carrier = robot.carrier
mp2 = carrier["MP 2Pos Fixed"]
mp3 = carrier["MP 3Pos Fixed"]
shelf = carrier["Shelf 8x4Pos"]
mp_3pos_deck = carrier["MP 3Pos Deck"]
mca_4pos = carrier["MCA96 Diti 4Pos"]

# Make positions
lid1_pos = mp2.site(0)
lid2_pos = mp2.site(1)
plate1_pos = mp3.site(0)
plate2_pos = mp3.site(1)
dil_pos = mp3.site(2)


# Plates
strainplate = Plate(name="strain", start_position=robot.storex_site,
                    labware=labwares["greiner384"], incubating=True, storex_cart=1, cart_site=1)
exponential_plate = Plate(name="assay_1", start_position=robot.storex_site,
                          labware=labwares["greiner384"], incubating=True, storex_cart=1, cart_site=2)
assayplate = Plate(name="assay_1", start_position=robot.storex_site,
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
robot.mca.add_tips(ditis_1)