from pypetting_extra import Plate


def make_plates_with_paths(n, experiment, robot, n_max=20):
    plates = []
    paths = []
    site, c = 1, 1
    for i in range(n):
        if site >= n_max:
            site = 1
            c += 1
        else:
            site += 1
        paths.append(
            experiment.windows_paths["img"] + "\\plate_"+str(i)+".png")
        plates.append(Plate(name="plate_"+str(i), start_position=robot.storex_site,
                            labware=Labware("Agar Spot Plate", 8, 1), incubating=True, storex_cart=c, cart_site=site))
    return plates, paths
