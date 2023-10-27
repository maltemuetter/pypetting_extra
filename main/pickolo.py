from .base import direct_command


class Pickolo:
    def __init__(self, light_table, windows_pickolo_path, pickolo_profile_name):
        self.position = light_table.site(0)
        self.windows_pickolo_path = windows_pickolo_path
        self.profile_name = pickolo_profile_name
        self.pickolo_open = False

    def take_photo(self, windows_img_path, close_pickolo=True,  capture_cmd=" -c -o "):
        WL = []
        if not self.pickolo_open:
            WL += self.open()
        WL += [self.pickolo_command(capture_cmd, windows_img_path)]
        if close_pickolo:
            WL += self.close()
        return WL

    def open(self):
        WL = []
        WL.append(self.pickolo_command(" -i"))
        WL.append(self.pickolo_command(
            " -p " + self.profile_name))
        WL.append(self.pickolo_command(" -c"))
        self.pickolo_open = True
        return WL

    def close(self, closing_cmd=" -T"):
        self.pickolo_open = False
        return [self.pickolo_command(closing_cmd)]

    def pickolo_command(self, cmd: str, img_path: str = ""):
        return direct_command('Execute(' + self.windows_pickolo_path + cmd + img_path + ',2,"py_return",2);')
