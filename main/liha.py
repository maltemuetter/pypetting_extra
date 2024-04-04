from .base import direct_command
import numpy as np
from pypetting import aspirate, dispense, wash, move_liha, GridSite
import math
from numpy.typing import ArrayLike


class LiHA:
    def __init__(self):
        self.all_tips = np.array([True] * 8)
        self.minimal_fd = "Minimal FD"
        self.tip_vol_max = 250

    def aspirate(
        self,
        plate,
        col,
        volumes,
        column_mask,
        liquid_class="Minimal CD ZMAX",
        tip_array=8 * [True],
        waste_volume=0,
        retract=True,
    ):
        wl = [
            aspirate(
                plate.gridsite,
                col,
                list(column_mask),
                (volumes + waste_volume) * np.array(tip_array),
                liquid_class,
                labware=plate.labware,
            )
        ]

        if retract:
            wl += [
                move_liha(
                    plate.gridsite,
                    col,
                    column_mask,
                    tip_array=tip_array,
                    local=True,
                    spacing=plate.labware.spacing,
                    labware=plate.labware,
                )
            ]
        return wl

    def dispense(
        self,
        plate,
        col,
        volumes,
        column_mask,
        liquid_class="Minimal CD ZMAX",
        tip_array=8 * [True],
        retract=True,
    ):
        wl = [
            dispense(
                plate.gridsite,
                col,
                list(column_mask),
                volumes * np.array(tip_array),
                liquid_class,
                labware=plate.labware,
            )
        ]
        if retract:
            wl += [
                move_liha(
                    plate.gridsite,
                    col,
                    column_mask,
                    tip_array=tip_array,
                    local=True,
                    spacing=plate.labware.spacing,
                    labware=plate.labware,
                )
            ]
        return wl

    def move_liha_to_lighttable(self):
        return direct_command('MoveLiha(1,46,0,1,"01011",0,4,0,10,0,0);')
        # If time replace with correct comand defined by the plate pos.

    # return move_liha(self.pickolo.camera_position, 1)

    def move_liha(
        self,
        plate,
        column_mask,
        column=1,
        spacing=1,
        tip_array=8 * [True],
        local: bool = False,
        z_pos: int = 0,
        speed: int = 10,
    ):

        return [
            move_liha(
                plate.gridsite,
                column,
                column_mask,
                tip_array=tip_array,
                local=local,
                spacing=spacing,
                z_pos=z_pos,
                speed=speed,
            )
        ]

    def simple_wash(self):
        h2o2 = GridSite(30, 1, "")
        ethanol = GridSite(30, 2, "")

        water = "sterileWash_N_H2O"
        etoh = "sterileWash_N_EtOH"

        WL = [
            wash(1, 0.1, 31),
            aspirate(
                ethanol,
                1,
                self.all_tips,
                900 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            dispense(
                ethanol,
                1,
                self.all_tips,
                900 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            wash(2, 1, 31),
            aspirate(
                ethanol,
                1,
                self.all_tips,
                900 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            dispense(
                ethanol,
                1,
                self.all_tips,
                900 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            aspirate(
                h2o2, 1, self.all_tips, 900 * self.all_tips, water, labware="trough100"
            ),
            dispense(
                h2o2, 1, self.all_tips, 900 * self.all_tips, water, labware="trough100"
            ),
            move_liha(
                ethanol, 1, column_mask=8 * [True], local=True, labware="trough100"
            ),
        ]
        return WL

    def mix(
        self,
        plate,
        col,
        volumes,
        cycles,
        column_mask,
        tip_array=8 * [True],
        liquid_class="Minimal CD ZMAX",
    ):
        worklist = []
        for _ in range(cycles):
            worklist += self.aspirate(
                plate,
                col,
                volumes,
                column_mask,
                tip_array=tip_array,
                liquid_class=liquid_class,
                waste_volume=0,
                retract=False,
            )
            worklist += self.dispense(
                plate,
                col,
                volumes,
                column_mask,
                tip_array=tip_array,
                liquid_class=liquid_class,
            )
        return worklist

    def dilution_row(
        self,
        plate,
        column_mask,
        well_volume: int = 250,
        start_col: int = 1,
        stop_at_col: int = 12,
        n_mix: int = 3,
        tip_array=8 * [True],
        dilution_factor=10,
        liquid_class="Minimal FD",
        liquid_class_asp="Minimal CD ZMAX",
    ):
        mix_volume = 0.6 * well_volume
        transfer_volume = well_volume / dilution_factor
        worklist = []
        for i in range(start_col, stop_at_col):
            worklist += self.aspirate(
                plate,
                i,
                transfer_volume,
                column_mask,
                liquid_class=liquid_class_asp,
            )
            worklist += self.dispense(
                plate,
                i + 1,
                transfer_volume,
                column_mask,
                liquid_class=liquid_class,
            )
            worklist += self.mix(
                plate, i + 1, mix_volume, n_mix, column_mask, tip_array=tip_array
            )
            worklist += self.simple_wash()
        return worklist

    def fill_96_well_plate(
        self,
        src_plate,
        dest_plate,
        fill_volume,
        column_mask,
        start_col=1,
        end_col=12,
        src_col=1,
    ):
        n = math.floor(self.tip_vol_max / fill_volume)
        count = 0
        wl = []
        for i, dest_col in enumerate(range(start_col, end_col + 1)):
            if count == 0:
                di = len(range(start_col, end_col + 1)) - i
                wl.extend(
                    self.aspirate(
                        src_plate, src_col, min(n, di) * fill_volume, column_mask
                    )
                )
                count = n

            wl.extend(
                self.dispense(
                    dest_plate,
                    dest_col,
                    fill_volume,
                    column_mask,
                    liquid_class=self.minimal_fd,
                )
            )
            count -= 1
        return wl

    def fill_384_well_rep(
        self,
        src_plate,
        dest_plate,
        fill_volume,
        column_mask_dest,
        start_col=1,
        n_cols=12,
        src_col=1,
        step=2,
        column_mask_src=8 * [True],
    ):
        wl = []
        nmax = math.floor(self.tip_vol_max / fill_volume)
        count = 0
        for i, n in enumerate(range(n_cols)):
            dest_col = start_col + step * n
            if count == 0:
                di = len(range(n_cols)) - i

                wl.extend(
                    self.aspirate(
                        src_plate, src_col, min(di, nmax) * fill_volume, column_mask_src
                    )
                )
                count = nmax

            wl.extend(
                self.dispense(
                    dest_plate,
                    dest_col,
                    fill_volume,
                    column_mask_dest,
                    liquid_class=self.minimal_fd,
                )
            )
            count -= 1
        return wl

    def add_pickolo(self, pickolo):
        self.pickolo = pickolo

    def take_photo(self, img_name, close_pickolo=True):
        #  careful. This should be connected to the light table position... Replace if time...
        WL = [self.move_liha_to_lighttable()]
        WL += self.pickolo.take_photo(img_name, close_pickolo=close_pickolo)
        return WL

    def spot(self, plate, volume, column_mask, tip_array=np.array(8 * [True])):
        wl = self.dispense(
            plate,
            1,
            volume / 2,
            column_mask,
            tip_array=np.array(tip_array),
            liquid_class="Minimal CD Agar",
            retract=False,
        )

        wl += self.dispense(
            plate,
            2,
            volume / 2,
            column_mask,
            tip_array=np.array(tip_array),
            liquid_class="Minimal CD Agar",
            retract=False,
        )

        wl.append(self.move_liha_to_lighttable())
        return wl
