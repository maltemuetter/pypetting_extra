from pypetting_extra import robot, Experiment


def make_photo_of_plate(robot, plate, new_lid_pos, img_path, close_pickolo=True):
    WL = [robot.roma.move_plate_to_photo_position(plate, new_lid_pos)]
    WL += robot.liha.take_photo(img_path, close_pickolo=close_pickolo)
    WL += robot.roma.incubate_plate(plate)
    return WL


def make_photos_of_plates(robot, plates, new_lid_pos, worklist, add=""):
    for plate in plates:
        worklist.add(robot.roma.move_plate_to_photo_position(
            plate, new_lid_pos))
        worklist.add(robot.liha.take_photo(plate.name+add+".png",
                     close_pickolo=False), msg="pickolo:_"+plate.name)
        worklist.add(robot.roma.incubate_plate(plate))
    worklist.add(robot.pickolo.close())
