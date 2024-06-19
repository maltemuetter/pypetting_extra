from .base import direct_command
from pypetting import transfer_labware


class ROMA:
    def __init__(self):
        pass

    def move_roma_to_home(self):
        return direct_command("ROMA(2,80,75,0,0,0,150,1,0);")

    def add_incubator(self, storex):
        self.incubator = storex

    def add_plate_reader(self, reader):
        self.plate_reader = reader

    def add_pickolo(self, pickolo):
        self.pickolo = pickolo

    def instert_plate_to_reader(
        self, plate, new_lid_gridsite=None, end_with_covered_plate=True
    ):
        WL = []
        if not self.plate_reader.is_open:
            WL.append(self.plate_reader.open())
        WL += self.move_plate(
            plate,
            self.plate_reader.gridsite,
            new_lid_gridsite=new_lid_gridsite,
            end_with_covered_plate=end_with_covered_plate,
        )
        WL.append(self.plate_reader.close())
        plate.toggle_in_plate_reader()
        return WL

    def move_plate_to_photo_gridsite(self, plate, new_lid_gridsite):
        return self.move_plate(
            plate,
            self.pickolo.gridsite,
            new_lid_gridsite=new_lid_gridsite,
            end_with_covered_plate=False,
        )

    def incubate(self, plate):
        WL = self.move_plate(plate, self.incubator.gridsite)
        WL += self.incubator.incubate(plate)
        return WL

    def store(self, plate):
        WL = self.move_plate(plate, plate.store_pos)
        return WL

    def move_plate(
        self, plate, dest, new_lid_gridsite=None, end_with_covered_plate=True
    ):
        WL = []
        if plate.incubating:
            WL.append(self.incubator.present(plate))
        if plate.in_plate_reader:
            WL.append(self.plate_reader.open())
            close_reader = True
        else:
            close_reader = False

        src = plate.gridsite
        labw = plate.labware

        # lid handling
        if end_with_covered_plate:  #  handle_lid
            #  Open plate
            if plate.covered:  #  move closed plate
                WL.append(transfer_labware(src, dest, labw))
            else:  # close plate and move
                lid = plate.lid_gridsite
                WL.append(
                    transfer_labware(
                        src, dest, labw, cover=True, lid=plate.lid_gridsite
                    )
                )
            plate.update_lid_gridsite(dest)
        else:
            if plate.covered:  # open plate and move
                plate.lid_gridsite = lid = new_lid_gridsite
                WL.append(transfer_labware(src, dest, labw, cover=False, lid=lid))
                plate.update_lid_gridsite(new_lid_gridsite)
            else:  # move open plate
                WL.append(transfer_labware(src, dest, labw))

        plate.update_gridsite(dest)
        plate.covered = plate.gridsite == plate.lid_gridsite

        if close_reader:
            WL.append(self.plate_reader.close())
            plate.toggle_in_plate_reader()
        return WL
