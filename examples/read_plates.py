from pypetting_extra.custom_scripts.routines import make_photos_of_plates
from pypetting_extra import robot, Plate, Worklist
from pypetting import Labware


mp2 = robot.carrier["MP 2Pos Fixed"]
lid1_pos = mp2.site(0)

img_folder_path = "C:\\Users\\COMPUTER\\polybox\\Robot-Malte\\test\\img"

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
    paths.append(img_folder_path + "\\plate_"+str(i)+".png")
    plates.append(Plate(name="plate_"+str(i), start_position=robot.storex_site,
                        labware=Labware("Agar Spot Plate", 8, 1), incubating=True, storex_cart=c, cart_site=site))

photo_wl = Worklist("photo_wl.gwl")
photo_wl.add(make_photos_of_plates(robot, plates, lid1_pos, paths))
photo_wl.save()
