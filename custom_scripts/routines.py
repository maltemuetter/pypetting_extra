from pypetting_extra import robot


def make_photo_of_plate(robot, plate, new_lid_pos, img_path, close_pickolo=True):
    WL = [robot.roma.move_plate_to_photo_position(plate, new_lid_pos)]
    WL += robot.liha.take_photo(img_path, close_pickolo=close_pickolo)
    WL += robot.roma.incubate_plate(plate)
    return WL


def make_photos_of_plates(robot, plates, new_lid_pos, img_paths):
    WL = []
    for plate, img_path in zip(plates, img_paths):
        WL += robot.roma.move_plate_to_photo_position(plate, new_lid_pos)
        WL += robot.liha.take_photo(img_path, close_pickolo=False)
        WL += robot.roma.incubate_plate(plate)
    WL += robot.pickolo.close()
    return WL
