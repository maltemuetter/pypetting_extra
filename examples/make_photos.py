from pypetting_extra.custom_scripts.routines import make_photos_of_plates
from pypetting_extra import robot, Plate, Experiment, Protocol
from pypetting import Labware
from pypetting_extra.main.base import direct_command
from pypetting.labware import labwares
import os

exp_path = os.path.join(os.getcwd(), "experiments")
experiment = Experiment(
    "test", exp_path, "C:\\Users\\COMPUTER\\polybox\\Robot-Malte")
experiment.initialize()

protocol = Protocol(experiment, "timelog.csv")
mp2 = robot.carrier["MP 2Pos Fixed"]
lid1_pos = mp2.site(0)


shelf = robot.carrier[ 'Shelf 8x4Pos']
shelf.define_plate("dilutionplate", labwares["greiner96"], 30)

assayplate = robot.incubator.define_plate("assayplate", labwares["greiner384"], 1, 2)

cart_site_1 = robot.incubator.cart_site(1,1)
agarplate = cart_site.define_plate()


plates = []
paths = []
n = 25
n_max = 20
site, c = 1, 1
for i in range(n):
    if site >= n_max:
        site = 1
        c += 1
    else:
        site += 1
    paths.append(experiment.windows_paths["img"] + "\\plate_"+str(i)+".png")
    plates.append(Plate(name="plate_"+str(i), start_position=robot.storex_site,
                        labware=Labware("Agar Spot Plate", 8, 1), incubating=True, storex_cart=c, cart_site=site))

photo_wl = experiment.make_worklist("photo_wl.gwl")
photo_wl.add(make_photos_of_plates(robot, plates, lid1_pos, paths, protocol))
photo_wl.save()
