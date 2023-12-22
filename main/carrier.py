from pypetting import GridSite, Labware
from dataclasses import dataclass
from .sites import Site

@dataclass(frozen=True)
class Device:
    labware: Labware
    gridsite: GridSite


class Carrier:
    def __init__(self, name:str, grid:int, number_of_sites:int, incubator_carrier:bool = False, storex_gridsite = None, cart_num = None):
        self.name = name
        self.grid = grid
        self.sites = []
        self.incubator_carrier = incubator_carrier
        self.storex_gridsite = storex_gridsite
        self.cart_num = cart_num
        if incubator_carrier:
            self.create_sites(number_of_sites)
        else:
            self.create_sites(number_of_sites)

    def create_sites(self, number_of_sites):
        for i in range(number_of_sites):
                self.sites.append(Site(self.grid, self.name, i, incubating = self.incubator_carrier))

    def create_incubator_sites(self, number_of_sites):
        for i in range(number_of_sites):
                self.sites.append(Site(
                    self.storex_gridsite.grid, self.storex_gridsite.carrier, 0, incubating = True, cart_site=i, cart_num=self.cart_num))

    def define_plate(self, name:str, labware:Labware, site_idx:int, is_store_pos = False):
        site = self.site(site_idx)
        return site.define_plate(name, labware, is_store_pos = is_store_pos)

    def gridsite(self, site):
        return self.sites[site].gridsite
    
    def site(self, site_idx):
        return self.sites[site_idx]

    def define_labware(self, labware, site):
        gridsite = GridSite(grid=self.grid, carrier=self.name, site=site)
        return Device(labware=labware, gridsite=gridsite)
    
    def get_free_sites(self):
        free = []
        for site in self.sites:
            if site.free:
                free.append(site)
        return free

    def __str__(self):
        return (f"Carrier(name={self.name}, "
                f"grid={self.grid}, "
                f"number_of_sites={len(self.sites)}, "
                f"incubator_carrier={self.incubator_carrier})")

    def __repr__(self):
        return (f"Carrier(name={self.name!r}, "
                f"grid={self.grid}, "
                f"number_of_sites={len(self.sites)}, "
                f"incubator_carrier={self.incubator_carrier}, "
                f"storex_gridsite={self.storex_gridsite}, "
                f"cart_num={self.cart_num})")

