from .base import direct_command
import numpy as np
from pypetting import (aspirate, dispense, wash, move_liha, GridSite)
import math


class LiHA:
    def __init__(self, minimal_cd="Minimal CD ZMAX", liha_mix="LB CD ZMAX FAST", minimal_fd="Minimal FD", waste_volume=0):
        self.waste_volume = waste_volume
        self.all_tips = np.array([True] * 8)
        self.tip_array = np.ones(8, dtype=bool)
        self.standard_liquid_class = minimal_cd
        self.minimal_fd = minimal_fd
        self.liquid_class_mix = liha_mix

    def aspirate(self, plate, col, volumes, liquid_class=False, column_mask=False, tip_array=False, waste_volume="default"):
        if waste_volume == "default":
            waste_volume = self.waste_volume
        else:
            waste_volume = waste_volume

        tip_array, liquid_class, column_mask = self.fill_standard_params(
            plate, liquid_class, tip_array, column_mask)

        WL = [aspirate(plate.position,
                       col,
                       column_mask,
                       (volumes+waste_volume)*tip_array,
                       liquid_class,
                       labware=plate.labware,
                       spacing=plate.labware.spacing)]
        if waste_volume != 0:
            WL += [dispense(plate.position,
                            col,
                            column_mask,
                            waste_volume*tip_array,
                            liquid_class=self.minimal_fd,
                            labware=plate.labware,
                            spacing=plate.labware.spacing)]
        return WL

    def dispense(self, plate, col, volumes, liquid_class=False, tip_array=False, column_mask=False):
        tip_array, liquid_class, column_mask = self.fill_standard_params(
            plate, liquid_class, tip_array, column_mask)
        return [dispense(plate.position,
                         col,
                         column_mask,
                         volumes*tip_array,
                         liquid_class,
                         labware=plate.labware,
                         spacing=plate.labware.spacing)]

    def move_liha_to_lighttable(self):
        return direct_command('MoveLiha(1,46,0,1,"01011",0,4,0,10,0,0);')

    def move_liha(self, plate, column=1):
        return move_liha(plate.position, column)

    def simple_wash(self):
        ethanol1 = GridSite(30, 0, "")
        h2o2 = GridSite(30, 1, "")
        ethanol = GridSite(30, 2, "")

        water = "sterileWash_N_H2O"
        etoh = "sterileWash_N_EtOH"

        WL = [wash(1, 0.1, 32),
              aspirate(ethanol1, 1, self.all_tips, 300 * self.all_tips,
                       etoh, labware="trough100"),
              dispense(ethanol1, 1, self.all_tips, 300 * self.all_tips,
                       etoh, labware="trough100"),
              wash(1, 0.1, 31), wash(2, 1, 31),
              aspirate(h2o2, 1, self.all_tips, 450 * self.all_tips,
                       water, labware="trough100"),
              dispense(h2o2, 1, self.all_tips, 450 * self.all_tips,
                       water, labware="trough100"),
              move_liha(ethanol, 1, local=True, labware="trough100")]
        return WL

    def mix(self, plate, col, volume, cycles,  liquid_class=False, column_mask=False, tip_array=False):
        tip_array, liquid_class, column_mask = self.fill_standard_params(
            plate, liquid_class, tip_array, column_mask)
        for _ in range(cycles):
            worklist = self.aspirate(
                plate, col, volume, tip_array=tip_array, liquid_class=liquid_class, column_mask=column_mask, waste_volume=0)
            worklist += self.dispense(plate, col, volume, tip_array=tip_array,
                                      liquid_class=self.minimal_fd, column_mask=column_mask)
        return worklist

    def dilution_row(self, plate, well_volume=200, stop_at_col=12, n_mix=3, tip_array=False, dilution_factor=10, liquid_class=False, column_mask=False):
        tip_array, liquid_class, column_mask = self.fill_standard_params(
            plate, liquid_class, tip_array, column_mask)
        mix_volume = 0.6*well_volume
        transfer_volume = well_volume/dilution_factor
        worklist = self.simple_wash()
        for i in range(stop_at_col-1):
            worklist += self.aspirate(plate, i+1,
                                      transfer_volume*tip_array, liquid_class=liquid_class, column_mask=column_mask)
            worklist += self.dispense(plate, i+2,
                                      transfer_volume*tip_array, "Minimal CD ZMAX", column_mask=column_mask)
            worklist += self.mix(plate, i+2, mix_volume, n_mix,
                                 tip_array=tip_array, column_mask=column_mask)
            worklist += self.simple_wash()
        return worklist

    def fill_96_well_plate(self, src_plate, dest_plate, fill_volume, start_col=1, end_col=12):
        wl = self.simple_wash()
        vmax = 950
        n = math.floor(vmax/fill_volume)
        count = 0
        for col in range(start_col, end_col):
            if count == 0:
                wl.extend(self.aspirate(src_plate, 1, n*fill_volume))
                count = n

            wl.extend(self.dispense(dest_plate, col,
                      fill_volume, liquid_class=self.minimal_fd))
            count -= 1
        wl.extend(self.simple_wash())
        return wl

    def fill_standard_params(self, plate, liquid_class, tip_array, column_mask):
        if type(column_mask) != list:
            rows = plate.labware.rows
            if rows == 8:
                column_mask = 8*[True]
            elif rows == 16:
                column_mask = 8*[True, False]
            else:
                Exception("pls provide column mask")
        if not liquid_class:
            liquid_class = self.standard_liquid_class
        if type(tip_array) != list:
            tip_array = self.tip_array
        return tip_array, liquid_class, column_mask

    def add_pickolo(self, pickolo):
        self.pickolo = pickolo

    def take_photo(self, img_path, close_pickolo=True):
        #  careful. This should be connected to the light table position... Replace if time...
        WL = [direct_command('MoveLiha(1,46,0,1,"01011",0,4,0,10,0,0);')]
        WL += self.pickolo.take_photo(img_path, close_pickolo=close_pickolo)
        return WL

    def close_pickolo(self):
        return [self.pickolo.close_pickolo()]

    def set_minimal_cd(self, minimal_cd):
        self.standard_liquid_class = minimal_cd

    def set_liha_mix(self, liha_mix):
        self.liquid_class_mix = liha_mix

    def set_minimal_fd(self, minimal_fd):
        self.minimal_fd = minimal_fd

    def set_liha_agar(self, liha_Agar):
        self.liha_Agar = liha_Agar

    def set_zmax(self, ZMax):
        self.ZMax = ZMax

    def set_waste_volume(self, waste_volume):
        self.waste_volume = waste_volume
