from pypetting import GridSite
import numpy as np


class Plate:
    def __init__(self,
                 name: str,
                 labware,
                 start_position: GridSite,
                 incubating=False,
                 storex_cart=None,
                 cart_site=None,
                 store_pos=None):
        self.name = name
        self.labware = labware
        self.position = self.lid_position = start_position
        self.covered = True  #  Always start with a covered lid
        self.incubating = incubating
        self.in_plate_reader = False
        self.store_pos = store_pos

        if labware.spacing == 1:
            frag = [True]
        elif labware.spacing == 2:
            frag = [True, False]
        else:
            raise Exception("unknown well spacing")

        self.column_mask = np.array(frag*8)

        if incubating:
            self.storex_cart = storex_cart
            self.cart_site = cart_site

    def update_position(self, position):
        self.position = position

    def update_lid_position(self, lid_position):
        self.lid_position = lid_position

    def assign_storeX_positions(self, storex_cart, cart_site):
        self.cart_site = cart_site
        self.storex_cart = storex_cart

    def toggle_incubation_status(self):
        self.incubating = not self.incubating

    def toggle_in_plate_reader(self):
        self.in_plate_reader = not self.in_plate_reader
