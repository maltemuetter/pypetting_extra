from pypetting import GridSite, Labware
from dataclasses import dataclass
from .sites import Site, CartSite
import pandas as pd

@dataclass(frozen=True)
class Device:
    labware: Labware
    gridsite: GridSite

class ContainerMixin:
    def define_plate(self, name: str, labware: Labware, site_idx: int, is_store_pos=False):
        site = self.site(site_idx)
        return site.define_plate(name, labware, is_store_pos=is_store_pos)
    
    def define_plate_on_free_site(self, name: str, labware: Labware, is_store_pos=False):
        site = self.get_next_free_site()
        return site.define_plate(name, labware, is_store_pos=is_store_pos)

    def get_next_free_site(self):
        for site in self.sites:
            if not site.occupied:
                return site
        raise Exception("No Free Sites in that container")  # Use raise instead of Exception as a statement

    def is_full(self):
        return all(site.occupied for site in self.sites)

    def get_free_sites(self):
        return [site for site in self.sites if not site.occupied]

    def gridsite(self, site):
        return self.sites[site].gridsite
    
    def site(self, site_idx):
        return self.sites[site_idx]

    def define_labware(self, labware, site):
        gridsite = GridSite(grid=self.grid, carrier=self.name, site=site)
        return Device(labware=labware, gridsite=gridsite)


class Carrier(ContainerMixin):
    def __init__(self, name:str, grid:int, number_of_sites:int,  storex_gridsite = None, cart_num = None):
        self.name = name
        self.grid = grid
        self.sites = []
        self.storex_gridsite = storex_gridsite
        self.cart_num = cart_num
        self.create_sites(number_of_sites)

    def create_sites(self, number_of_sites):
        for i in range(number_of_sites):
                self.sites.append(Site(self.grid, self.name, i))
    
    def locations(self):
        locations = []
        for site in self.sites:
            carrier = self.name
            cart = None
            s = site.gridsite.site
            
            if site.occupied:
                labw = site.labware.name
            else:
                labw = None  

            locations.append({
                "site":s,
                "labware": labw, 
                "carrier": carrier,
                "cartridge":cart})
        return pd.DataFrame().from_records(locations)

    def __str__(self):
        return (f"Carrier(name={self.name}, "
                f"grid={self.grid}, "
                f"number_of_sites={len(self.sites)}")

    def __repr__(self):
        return (f"Carrier(name={self.name!r}, "
                f"grid={self.grid}, "
                f"number_of_sites={len(self.sites)}, "
                f"storex_gridsite={self.storex_gridsite}, "
                f"cart_num={self.cart_num})")



class Cartridge(ContainerMixin):
    def __init__(self, name:str, grid:int, number_of_sites:int,  storex_gridsite = None, cart_num = None):
        self.name = name
        self.grid = grid
        self.sites = []
        self.storex_gridsite = storex_gridsite
        self.cart_num = cart_num
        self.create_sites(number_of_sites)

    def create_sites(self, number_of_sites):
        for i in range(number_of_sites):
                self.sites.append(CartSite(
                    self.storex_gridsite.grid, self.storex_gridsite.carrier, i+1, self.cart_num))

    def locations(self):
        locations = []
        for site in self.sites:
            if site.occupied:
                labw = site.labware.name
            else:
                labw = None  

            locations.append({
                "site":site.cart_site,
                "labware": labw, 
                "carrier": "StoreX",
                "cartridge":self.name})
        return pd.DataFrame().from_records(locations)

    def __str__(self):
        return (f"Cartrdige(name={self.name}, "
                f"grid={self.grid}, "
                f"number_of_sites={len(self.sites)}")

    def __repr__(self):
        return (f"Cartrdige(name={self.name!r}, "
                f"grid={self.grid}, "
                f"number_of_sites={len(self.sites)}, "
                f"storex_gridsite={self.storex_gridsite}, "
                f"cart_num={self.cart_num})")

