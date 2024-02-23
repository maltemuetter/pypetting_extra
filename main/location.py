import pandas as pd


class Location:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.DataFrame(columns = ["name", "carrier", "cartridge", "site", "labware"])

    def add(self, plates):
        if type(plates) == list:
            for plate in plates:
                self.add_labware(plate)
        else:
            self.add_labware(plates)
        self.save()

    def add_labware(self, plate):
        gridsite = plate.gridsite
        if gridsite.carrier == "StoreX 22Pos":
            row = {
                "name" : plate.name,
                "carrier":gridsite.carrier,
                "cartridge" : plate.storex_cart,
                "site" : plate.cart_site,
                "labware" : plate.labware.name
                    }
        else:
            row = {
                "name" : plate.name,
                "carrier":gridsite.carrier,
                "cartridge":None,
                "site" : gridsite.site + 1, 
                "labware" : plate.labware.name
            }
        self.df = pd.concat([self.df, pd.DataFrame([row])])
         

    def save(self):
        self.df.to_csv(self.filepath, index=False)
