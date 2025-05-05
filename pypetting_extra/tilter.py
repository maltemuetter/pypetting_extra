from .base import direct_command
from .container import ContainerMixin
from pypetting import wait_timer, start_timer, GridSite
from .sites import Site


class PlateTilter(ContainerMixin):
    def __init__(self, name, grid, number_of_sites=1):
        self.name = name
        self.grid = grid
        self.sites = []
        self.create_sites(number_of_sites)

    def create_sites(self, number_of_sites):
        for i in range(number_of_sites):
            self.sites.append(Site(self.grid, self.name, i))

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
