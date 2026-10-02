from .roma import ROMA
from .liha import LiHA
from .mca import MCA
from .platereader import InfinitePlateReader
from .storex import StoreX
from .container import Carrier
from pypetting import GridSite


class Worktable:
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

    def add_tips(self, ditis):
        self.mca.add_tips(ditis)

    def return_tools(self):
        return self.roma, self.liha, self.mca, self.plate_reader

    def add_carrier(self, name, grid, capacity):
        self.carrier.update({name: Carrier(name, grid, capacity)})
        self.carrier_names.append(name)

    def add_pintool_setup(self, pintool_setup):
        self.pintool_setup = pintool_setup
        self.mca.add_pintool_setup(pintool_setup)

    def add_pickolo(self, pickolo):
        self.pickolo = pickolo
        self.roma.add_pickolo(pickolo)
        self.liha.add_pickolo(pickolo)

    def add_tilter(self, tilter):
        self.tilter = tilter

    def assign_pickolo_img_path(self, windows_img_folder_path):
        self.pickolo.set_img_folder(windows_img_folder_path)

    def setup_liha_wash(self, ethanol1, ethanol2, water):
        self.liha.setup_wash(ethanol1, ethanol2, water)
