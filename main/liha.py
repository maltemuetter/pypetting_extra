from .base import direct_command
import numpy as np
from pypetting import (aspirate, dispense, wash, move_liha, GridSite)
import math



class LiHA:
    def __init__(self):
        self.all_tips = np.array([True] * 8)
        self.minimal_fd = "Minimal FD"
        self.liquid_mix = "LB CD ZMAX FAST"

    def aspirate(self, plate, col, volumes, column_mask, liquid_class="Minimal CD ZMAX", tip_array = 8*[True], waste_volume=0):
        WL = [aspirate(plate.gridsite,
                       col,
                       list(column_mask),
                       (volumes+waste_volume)*np.array(tip_array),
                       liquid_class,
                       labware=plate.labware,
                       spacing=plate.labware.spacing)]
        if waste_volume != 0:
            WL += [dispense(plate.gridsite,
                            col,
                            list(column_mask),
                            waste_volume*np.array(tip_array),
                            liquid_class=self.minimal_fd,
                            labware=plate.labware,
                            spacing=plate.labware.spacing)]
        return WL
    
    def dispense(self, plate, col, volumes, column_mask, liquid_class="Minimal CD ZMAX", tip_array = 8*[True]):
        return [dispense(plate.gridsite,
                         col,
                         list(column_mask),
                         volumes*np.array(tip_array),
                         liquid_class,
                         labware=plate.labware,
                         spacing=plate.labware.spacing)]

    def move_liha_to_lighttable(self):
        return direct_command('MoveLiha(1,46,0,1,"01011",0,4,0,10,0,0);')
        # If time replace with correct comand defined by the plate pos.
       # return move_liha(self.pickolo.camera_position, 1)

    def move_liha(self, plate, column=1):
        return move_liha(plate.gridsite, column)

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

    def mix(self, plate, col, volumes, cycles,  column_mask, tip_array=8*True):
        worklist = []
        for _ in range(cycles):
            worklist += self.aspirate(
                plate, col, volumes,column_mask, tip_array=tip_array, liquid_class=self.liquid_mix, waste_volume=0)    
            worklist += self.dispense(plate, col, volumes, column_mask, tip_array=tip_array,
                                      liquid_class=self.minimal_fd)
        return worklist

    def dilution_row(self, plate, column_mask, well_volume=200, start_col=1, stop_at_col=12, n_mix=3, tip_array=8*[True], dilution_factor=10, liquid_class="Minimal CD ZMAX"):
        mix_volume = 0.6*well_volume
        transfer_volume = well_volume/dilution_factor
        worklist = []
        for i in range(start_col, stop_at_col):
            print(i, "to", i+1)
            worklist += self.aspirate(plate, i,
                                      transfer_volume*tip_array, column_mask, liquid_class=liquid_class)
            worklist += self.dispense(plate, i+1,
                                      transfer_volume*tip_array, column_mask, liquid_class = liquid_class)
            worklist += self.mix(plate, i+1, mix_volume, n_mix, column_mask,
                                 tip_array=tip_array)
            worklist += self.simple_wash()
        return worklist

    def fill_96_well_plate(self, src_plate, dest_plate, fill_volume, column_mask, start_col=1, end_col=12, src_col=1):
        wl = self.simple_wash()
        vmax = 950
        n = math.floor(vmax/fill_volume)
        count = 0
        for col in range(start_col, end_col):
            if count == 0:
                wl.extend(self.aspirate(src_plate, src_col, n*fill_volume, column_mask))
                count = n

            wl.extend(self.dispense(dest_plate, col,
                      fill_volume, column_mask, liquid_class=self.minimal_fd))
            count -= 1
        wl.extend(self.simple_wash())
        return wl

    def add_pickolo(self, pickolo):
        self.pickolo = pickolo

    def take_photo(self, img_name, close_pickolo=True):
        #  careful. This should be connected to the light table position... Replace if time...
        WL = [self.move_liha_to_lighttable()]
        WL += self.pickolo.take_photo(img_name, close_pickolo=close_pickolo)
        return WL

    def spot(self, plate, volume, column_mask, tip_array = np.array(8*[True])):
        wl = self.dispense(
                plate,
                1,
                volume/2,
                column_mask,
                tip_array=np.array(tip_array),
                liquid_class="Minimal CD Agar"
            )
        
        wl += self.dispense(
                plate,
                2,
                volume/2,
                column_mask,
                tip_array=np.array(tip_array),
                liquid_class="Minimal CD Agar"
            )
        
        wl.append(
            self.move_liha_to_lighttable()
        )
        return wl