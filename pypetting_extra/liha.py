from .base import direct_command
import numpy as np
from pypetting import aspirate, dispense, wash, move_liha, GridSite
import math
from numpy.typing import ArrayLike
from icecream import ic


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
        check_vol=True,
    ):

        if check_vol:
            if type(volumes) == int:
                if volumes > 250:
                    raise Exception(
                        f"use liha only for aspirating max 250 ul per tip. volume: {volumes}"
                    )

        if plate.rotated:
            if plate.labware_rotated is None:
                raise Exception("Rotated labware not defined.")
            labware = plate.labware_rotated
        else:
            labware = plate.labware
        self.column_labware_check(labware, column_mask)

        wl = [
            aspirate(
                plate.gridsite,
                col,
                list(column_mask),
                (volumes + waste_volume) * np.array(tip_array),
                liquid_class,
                labware=labware,
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
                    spacing=labware.spacing,
                    labware=labware,
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
        if plate.rotated:
            if plate.labware_rotated is None:
                raise Exception("Rotated labware not defined.")
            labware = plate.labware_rotated
        else:
            labware = plate.labware

        self.column_labware_check(labware, column_mask)

        wl = [
            dispense(
                plate.gridsite,
                col,
                list(column_mask),
                volumes * np.array(tip_array),
                liquid_class,
                labware=labware,
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
                    spacing=labware.spacing,
                    labware=labware,
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

    def setup_wash(self, ethanol1, ethanol2, water):
        self.ethanol1 = ethanol1
        self.ethanol2 = ethanol2
        self.water = water

    def sterile_wash(self):
        WL = []
        WL += [wash(1, 0.3, 31)]
        WL += self.mix(self.ethanol1, 1, 300, 2, 8 * [True], check_vol=False)
        WL += [wash(2, 1, 31)]
        WL += self.mix(self.ethanol2, 1, 400, 2, 8 * [True], check_vol=False)
        WL += self.mix(self.water, 1, 400, 1, 8 * [True], check_vol=False)
        # print("Sterile wash deactivated for debugging.")
        return WL

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
                300 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            dispense(
                ethanol,
                1,
                self.all_tips,
                300 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            wash(2, 1, 31),
            aspirate(
                ethanol,
                1,
                self.all_tips,
                300 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            dispense(
                ethanol,
                1,
                self.all_tips,
                300 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            aspirate(
                h2o2, 1, self.all_tips, 300 * self.all_tips, water, labware="trough100"
            ),
            dispense(
                h2o2, 1, self.all_tips, 300 * self.all_tips, water, labware="trough100"
            ),
            move_liha(
                ethanol, 1, column_mask=8 * [True], local=True, labware="trough100"
            ),
        ]
        return WL

    def fast_wash(self):
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
                300 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            dispense(
                ethanol,
                1,
                self.all_tips,
                300 * self.all_tips,
                etoh,
                labware="trough100",
            ),
            wash(2, 1, 31),
            aspirate(
                h2o2, 1, self.all_tips, 250 * self.all_tips, water, labware="trough100"
            ),
            dispense(
                h2o2, 1, self.all_tips, 250 * self.all_tips, water, labware="trough100"
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
        liquid_class="LB CD ZMAX FAST",
        check_vol=True,
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
                check_vol=check_vol,
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

    def vol_transfer(
        self,
        src_plate,
        src_col,
        dest_plate,
        dest_col,
        transfer_vol,
        column_mask,
        src_column_mask=None,
        liquid_class="Minimal CD ZMAX",
        tip_array=8 * [True],
        retract=True,
    ):
        if src_column_mask is None:
            src_column_mask = column_mask
        n = math.ceil(transfer_vol / self.tip_vol_max)
        wl = []
        rest_vol = transfer_vol
        for _ in range(n):
            vol = min(rest_vol, self.tip_vol_max)
            wl.extend(
                self.aspirate(
                    src_plate,
                    src_col,
                    vol,
                    src_column_mask,
                    liquid_class=liquid_class,
                    tip_array=tip_array,
                    retract=False,
                )
            )
            wl.extend(
                self.dispense(
                    dest_plate,
                    dest_col,
                    vol,
                    column_mask,
                    liquid_class=liquid_class,
                    tip_array=tip_array,
                    retract=retract,
                )
            )
            rest_vol = rest_vol - vol
        return wl

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
        liquid_class="LB CD ZMAX FAST",
    ):
        mix_volume = min(self.tip_vol_max, 0.5 * well_volume)
        transfer_volume = well_volume / dilution_factor
        worklist = []
        for i in range(start_col, stop_at_col):
            worklist += self.vol_transfer(
                plate,
                i,
                plate,
                i + 1,
                transfer_volume,
                column_mask,
                liquid_class=liquid_class,
                tip_array=tip_array,
            )

            worklist += self.mix(
                plate, i + 1, mix_volume, n_mix, column_mask, tip_array=tip_array
            )
            worklist += self.sterile_wash()
        return worklist

    def fill_96_well_plate(
        self,
        src_plate,
        dest_plate,
        fill_volume,
        column_mask,
        liquid_class="Minimal FD",
        tip_array=8 * [True],
        start_col=1,
        end_col=12,
        src_col=1,
        skip=0,
    ):
        return self.fill_plate(
            src_plate,
            dest_plate,
            fill_volume,
            column_mask,
            column_mask,
            liquid_class=liquid_class,
            tip_array=tip_array,
            start_col=start_col,
            end_col=end_col,
            src_col=src_col,
            skip=skip,
        )

    def fill_plate(
        self,
        src_plate,
        dest_plate,
        fill_volume,
        src_column_mask,
        dest_column_mask,
        liquid_class="Minimal FD",
        tip_array=8 * [True],
        start_col=1,
        end_col=12,
        src_col=1,
        skip=0,
        reverse_order=False,
        allow_multidispense=False,
    ):
        columns = list(range(start_col, end_col + 1, 1 + skip))
        if reverse_order:
            columns = columns[::-1]
        if fill_volume > self.tip_vol_max or not allow_multidispense:
            return self._fill_one_by_one(
                src_plate,
                dest_plate,
                fill_volume,
                src_column_mask,
                dest_column_mask,
                liquid_class,
                tip_array,
                columns,
                src_col,
            )
        return self._fill_bulk(
            src_plate,
            dest_plate,
            fill_volume,
            src_column_mask,
            dest_column_mask,
            liquid_class,
            tip_array,
            columns,
            src_col,
        )

    def _fill_one_by_one(
        self,
        src_plate,
        dest_plate,
        fill_volume,
        src_column_mask,
        dest_column_mask,
        liquid_class,
        tip_array,
        columns,
        src_col,
    ):
        wl = []
        for dest_col in columns:
            wl.extend(
                self.vol_transfer(
                    src_plate,
                    src_col,
                    dest_plate,
                    dest_col,
                    fill_volume,
                    dest_column_mask,
                    src_column_mask=src_column_mask,
                    liquid_class=liquid_class,
                    tip_array=tip_array,
                    retract=dest_col == columns[-1],
                )
            )
        return wl

    def _fill_bulk(
        self,
        src_plate,
        dest_plate,
        fill_volume,
        src_column_mask,
        dest_column_mask,
        liquid_class,
        tip_array,
        columns,
        src_col,
    ):
        wl = []
        counter = 0
        wells_per_aspirate = math.floor(self.tip_vol_max / fill_volume)
        for i, dest_col in enumerate(columns):
            if counter == 0:
                remaining = len(columns) - i
                n = min(remaining, wells_per_aspirate)
                wl.extend(
                    self.aspirate(
                        src_plate,
                        src_col,
                        n * fill_volume,
                        src_column_mask,
                        liquid_class=liquid_class,
                        tip_array=tip_array,
                    )
                )
                counter = n
            counter -= 1
            wl.extend(
                self.dispense(
                    dest_plate,
                    dest_col,
                    fill_volume,
                    dest_column_mask,
                    liquid_class=liquid_class,
                    tip_array=tip_array,
                    retract=counter == 0,
                )
            )
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

    @staticmethod
    def column_labware_check(labware, column_mask):
        if not len(column_mask) == labware.rows:
            Exception("column_mask doesnt fit number of plate rows.")
