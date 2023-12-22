from pypetting.base import GridSite
from pypetting import Labware
from pypetting.storex import return_plate, present_plate
from .carrier import Carrier

class StoreX:
    def __init__(self, gridsite=GridSite(grid=68, carrier="StoreX 22Pos", site=0), cartridge_capacities =[22, 22, 22, 22, 22] ):
        self.gridsite = gridsite
        self.cartridge_capacities = cartridge_capacities
        self.cartridges = []
        self.make_cartridges()

    def make_cartridges(self):
        for i, capacity in enumerate(self.cartridge_capacities):
            cart_num = i+1
            self.cartridges.append(
                self.make_cartridge(cart_num, capacity)
            )

    def define_plate(self, name:str, labware:Labware, cart_num:int, site_idx:int):
        site = self.site(cart_num, site_idx)
        return site.define_plate(name, labware)
    
    def site(self,cart_num, site_idx):
        return self.cartridges[cart_num].site(site_idx)

    def make_cartridge(self, cart_num, capacity):
        name = "cart_"+str(cart_num)
        cartridge = Carrier(
            name,
            self.gridsite.grid,
            capacity,
            incubator_carrier = True,
            storex_gridsite = self.gridsite,
            cart_num = cart_num
        )
        return cartridge

    def incubate(self, plate):
        WL = [return_plate(plate.storex_cart, plate.cart_site)]
        plate.toggle_incubation_status()
        return WL
    

    def present(self, plate):
        plate.toggle_incubation_status()
        return present_plate(plate.storex_cart,
                             plate.cart_site,
                             plate.labware)

