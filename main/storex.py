from pypetting.base import GridSite
from pypetting import Labware
from pypetting.storex import return_plate, present_plate
from .container import Cartridge
import pandas as pd


class StoreX:
    def __init__(
        self,
        gridsite=GridSite(grid=68, carrier="StoreX 22Pos", site=0),
        cartridge_capacities=[22, 22, 22, 22, 22],
    ):
        self.gridsite = gridsite
        self.cartridge_capacities = cartridge_capacities
        self.cartridges = []
        self.make_cartridges()

    def make_cartridges(self):
        for cart_idx, capacity in enumerate(self.cartridge_capacities):
            cart_num = cart_idx + 1
            self.cartridges.append(self.make_cartridge(cart_num, capacity))

    def get_next_free_cart(self):
        for cart in self.cartridges:
            if not cart.is_full():
                return cart
        raise Exception("All cartridges are full")

    def define_plate_next_free_site(self, name, labware):
        cartridge = self.get_next_free_cart()
        return cartridge.define_plate_on_free_site(name, labware)

    def define_plate(self, name: str, labware: Labware, cart_idx: int, site_idx: int):
        site = self.site(cart_idx, site_idx)
        return site.define_plate(name, labware)

    def site(self, cart_idx, site_idx):
        return self.cartridges[cart_idx].site(site_idx)

    def make_cartridge(self, cart_num, capacity):
        name = "cart_" + str(cart_num)
        cartridge = Cartridge(
            name,
            self.gridsite.grid,
            capacity,
            storex_gridsite=self.gridsite,
            cart_num=cart_num,
        )
        return cartridge

    def incubate(self, plate):
        WL = [return_plate(plate.storex_cart, plate.cart_site)]
        plate.toggle_incubation_status()
        return WL

    def present(self, plate):
        plate.toggle_incubation_status()
        return present_plate(plate.storex_cart, plate.cart_site, plate.labware)

    def locations(self):
        locations = []
        for cart in self.cartridges:
            locations.append(cart.locations())
        locations = pd.concat(locations)
        return locations.dropna()

    def replace_cartridge(self, cart_num, capacity):
        cart_idx = cart_num - 1
        self.cartridges[cart_idx] = self.make_cartridge(cart_idx, capacity)
