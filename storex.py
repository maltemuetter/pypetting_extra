from pypetting.base import GridSite
from pypetting.storex import return_plate, present_plate


class StoreX:
    def __init__(self, position=GridSite(grid=68, carrier="StoreX 22Pos", site=0)):
        self.position = position

    def incubate(self, plate):
        WL = [return_plate(plate.storex_cart, plate.cart_site)]
        plate.toggle_incubation_status()
        return WL

    def present(self, plate):
        plate.toggle_incubation_status()
        return present_plate(plate.storex_cart,
                             plate.cart_site,
                             plate.labware)
