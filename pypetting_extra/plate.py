from pypetting import GridSite
import numpy as np


class Plate:
    def __init__(
        self,
        name: str,
        labware,
        start_gridsite: GridSite,
        incubating=False,
        storex_cart=None,
        cart_site=None,
        store_pos=None,
    ):
        self.name = name
        self.labware = labware
        self.gridsite = self.lid_gridsite = start_gridsite
        self.covered = True  #  Always start with a covered lid
        self.incubating = incubating
        self.in_plate_reader = False
        self.store_pos = store_pos
        self.labware_rotated = None
        self.rotated = False

        if labware.spacing == 1:
            frag = [True]
        elif labware.spacing == 2:
            frag = [True, False]
        else:
            raise Exception("unknown well spacing")

        self.column_mask = np.array(frag * 8)

        if incubating:
            self.storex_cart = storex_cart
            self.cart_site = cart_site

    def update_rotation(self, dest_rotated):
        self.rotated = dest_rotated

    def update_gridsite(self, gridsite: GridSite):
        self.gridsite = gridsite

    def update_lid_gridsite(self, lid_gridsite: GridSite):
        self.lid_gridsite = self.lid_gridsite = lid_gridsite

    def assign_storeX_sites(self, storex_cart, cart_site):
        self.cart_site = cart_site
        self.storex_cart = storex_cart

    def add_rotated_labw(self, labware):
        self.labware_rotated = labware

    def toggle_incubation_status(self):
        self.incubating = not self.incubating

    def toggle_in_plate_reader(self):
        self.in_plate_reader = not self.in_plate_reader

    def __str__(self):
        return (
            f"Plate(name={self.name}, "
            f"gridsite={self.gridsite}, "
            f"covered={self.covered}, "
            f"incubating={self.incubating}, "
            f"in_plate_reader={self.in_plate_reader})"
        )

    def __repr__(self):
        return (
            f"Plate(\nname={self.name!r}, \n"
            f"labware={self.labware!r}, \n"
            f"current_gridsite={self.gridsite!r}, \n"
            f"incubating={self.incubating})"
        )
