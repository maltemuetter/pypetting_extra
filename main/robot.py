from pypetting_extra import ROMA, LiHA, MCA, InfinitePlateReader, StoreX, Carrier
from pypetting import Labware, GridSite


class Robot:
    def __init__(self):
        self.roma = ROMA()
        self.liha = LiHA()
        self.incubator = None
        self.mca = MCA()
        self.platereader = None
        self.pickolo = None
        self.carrier = {}
        self.carrier_names = []
        self.pintool = None

    def add_incubator(self, storex_site: GridSite):
        self.storex_site = storex_site
        self.incubator = StoreX(storex_site)
        self.roma.add_incubator(self.incubator)

    def add_plate_reader(self, reader_site: GridSite):
        self.reader_site = reader_site
        self.plate_reader = InfinitePlateReader(reader_site)
        self.roma.add_plate_reader(self.plate_reader)

    def add_pintool(self, pintool_setup):
        self.mca.add_pintool_setup(pintool_setup)

    def return_tools(self):
        return self.roma, self.liha, self.mca, self.plate_reader

    def add_carrier(self, name, position):
        self.carrier.update({name: Carrier(name, position)})
        self.carrier_names.append(name)

    def add_pintool_setup(self, pintool_setup):
        self.pintool_setup = pintool_setup
        self.mca.add_pintool_setup(pintool_setup)

    def add_pickolo(self, pickolo):
        self.pickolo = pickolo
        self.roma.add_pickolo(pickolo)
        self.liha.add_pickolo(pickolo)
