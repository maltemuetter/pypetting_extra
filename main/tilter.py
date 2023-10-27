from pypetting_extra.main.base import direct_command
from pypetting import wait_timer, start_timer


class PlateTilter:
    def __init__(self, name, grid, timer=3, tilt_time=25, self.recovery_time=10):
        self.name = name
        self.grid = grid
        self.timer = timer
        self.tilt_time = tilt_time

    def site(self, site):
        if site > 1:
            raise Exception("the tilter has only two positions.")
        return GridSite(grid=self.grid, carrier=self.name, site=site)

    def tilt(self):
        return [
            direct_command('Command("O2SSO2,1",1,1,,,2,2,0);'),
            start_timer(self.timer),
            wait_timer(self.timer, self.tilt_time),
            direct_command('Command("O2SSO2,0",1,1,,,2,2,0);]'),
            start_timer(self.timer),
            wait_timer(self.timer, self.recovery_time)
        ]
