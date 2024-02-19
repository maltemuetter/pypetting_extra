from pypetting_extra import Plate
from pypetting import Labware


def assign_incubator_plates(n, storex_site, labware, n_max=20, site_start=1, cart_start=1, prefix="plate_"):
    plates = []
    site, c = site_start, cart_start
    for i in range(n):
        if site > n_max:
            site = 1
            c += 1

        plates.append(Plate(name=prefix+str(i), start_gridsite=storex_site,
                            labware=labware, incubating=True, storex_cart=c, cart_site=site))
        site += 1
    return plates


def assign_shelf_plates_descending(n, shelf, labware, site_start=31, prefix="plate_"):
    plates = []
    site = site_start
    for i in range(n):
        plates.append(Plate(name=prefix + "_shelf" + str(site+1), start_gridsite=shelf.gridsite(site),
                            labware=labware, incubating=False, store_pos=shelf.gridsite(site)))
        site -= 1
    return plates
