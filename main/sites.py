from pypetting import GridSite
from .plate import Plate

class PositionMixin:
    def occupy(self, labware):
        self.labware = labware
        self.occupied = True
    
    def clear(self):
        self.occupied = False

class Site(PositionMixin):
    def __init__(self, grid: int, name: str, site: int):
        self.grid = grid
        self.carrier_name = name
        self.site = site
        self.occupied = False
        self.gridsite = GridSite(grid=grid, carrier=name, site=site)

    def define_plate(self, name, labware, is_store_pos=False):
        if is_store_pos:
            store_pos = self.gridsite
        else:
            store_pos = None
        plate = Plate(
            name=name, 
            start_gridsite=self.gridsite,
            labware=labware, 
            incubating=False, 
            store_pos=store_pos)
        self.occupy(plate)
        return plate

    def __str__(self):
        return f"Site(grid={self.grid}, name={self.carrier_name}, site={self.site}, occupied={self.occupied})"

class CartSite(PositionMixin):
    def __init__(self, grid: int, name: str, site: int, cart_num:int):
        self.grid = grid
        self.carrier_name = name
        self.site = site
        self.cart_num = cart_num
        self.occupied = False
        self.gridsite = GridSite(grid=grid, carrier=name, site=0)
        self.cart_site = site

    def define_plate(self, name, labware, is_store_pos=False):
        if is_store_pos:
            store_pos = self.gridsite
        else:
            store_pos = None
        plate = Plate(
            name=name, 
            start_gridsite=self.gridsite,
            labware=labware, 
            incubating=True, 
            storex_cart=self.cart_num, 
            cart_site=self.cart_site,
            store_pos=store_pos)
        self.occupy(plate)
        return plate

    def __str__(self):
        return f"CartSite(grid={self.grid}, name={self.carrier_name}, cart_site={self.cart_site}, occupied={self.occupied})"
