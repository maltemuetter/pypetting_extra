import pandas as pd


class Location:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.DataFrame(
            columns=["name", "carrier", "cartridge", "site", "labware"]
        )

    def add(self, plates):
        if type(plates) == list:
            for plate in plates:
                self.add_labware(plate)
        else:
            self.add_labware(plates)
        self.save()

    def add_labware(self, plate, labw_name=None, save=False):
        if not labw_name:
            labw_name = plate.labware.name
        gridsite = plate.gridsite
        if gridsite.carrier == "StoreX 22Pos":
            row = {
                "name": plate.name,
                "carrier": gridsite.carrier,
                "cartridge": plate.storex_cart,
                "site": plate.cart_site,
                "labware": labw_name,
            }
        else:
            row = {
                "name": plate.name,
                "carrier": gridsite.carrier,
                "cartridge": None,
                "site": gridsite.site + 1,
                "labware": labw_name,
            }
        self.df = pd.concat([self.df, pd.DataFrame([row])])
        if save:
            self.save()

    def save(self):
        self.df.to_csv(self.filepath, index=False)
