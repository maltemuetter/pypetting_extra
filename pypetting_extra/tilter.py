from .base import direct_command
from pypetting import wait_timer, start_timer, GridSite


class PlateTilter:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid

    def gridsite(self, site):
        return GridSite(grid=self.grid, carrier=self.name, site=site)

    def tilt(self, tilt_time=7, timer=3, recovery_time=8):
        return [
            direct_command('Command("O2SSO2,1",1,1,,,2,2,0);'),
            start_timer(timer),
            wait_timer(timer, tilt_time),
            direct_command('Command("O2SSO2,0",1,1,,,2,2,0);'),
            start_timer(timer),
            wait_timer(timer, recovery_time),
        ]
