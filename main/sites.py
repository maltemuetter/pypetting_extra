from pypetting import GridSite
from .plate import Plate

class Site:
    def __init__(self, grid:int, name:str, site:int, incubating:bool = False, cart_num = None):
        self.grid = grid
        self.carrier_name = name 
        self.occupied = False
        if incubating:
            self.gridsite = GridSite(grid = grid, carrier = name, site = 0)
            cart_site = site
        else:
            self.gridsite = GridSite(grid = grid, carrier = name, site = site)
            cart_site = None
        self.incubating = incubating
        self.cart_site = cart_site
        self.cart_num = cart_num

    def occupy(self, labware):
        self.labware = labware
        self.occupied = True
    
    def clear(self):
        self.occupied = False

    ## The first gridsite will be takes as home gridsite
    def define_plate(self, name, labware, is_store_pos = False):
        if is_store_pos:
            store_pos = self.gridsite
        else: 
            store_pos = None
        plate = Plate(
            name=name, 
            start_gridsite=self.gridsite,
            labware=labware, 
            incubating=self.incubating, 
            storex_cart=self.cart_num, 
            cart_site=self.cart_site,
            store_pos=store_pos)
        self.occupy(plate)
        return plate

    def __str__(self):
        return f"Site(grid={self.grid}, name={self.carrier_name}, occupied={self.occupied}, incubating={self.incubating})"

    def __repr__(self):
        return self.__str__()