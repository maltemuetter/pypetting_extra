from pypetting_extra import robot, Experiment


def make_photo_of_plate(robot, plate, new_lid_pos, img_path, close_pickolo=True):
    WL = [robot.roma.move_plate_to_photo_position(plate, new_lid_pos)]
    WL += robot.liha.take_photo(img_path, close_pickolo=close_pickolo)
    WL += robot.roma.incubate_plate(plate)
    return WL


def make_photos_of_plates(robot, plates, new_lid_pos, protocol, add=""):
    WL = []
    for plate in plates:
        WL += robot.roma.move_plate_to_photo_position(plate, new_lid_pos)
        WL += robot.liha.take_photo(plate.name+add, close_pickolo=False)
        WL += robot.roma.incubate_plate(plate)
        WL += [protocol.log_entry(plate.name + add)]
    WL += robot.pickolo.close()
    return WL
