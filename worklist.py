import os
from pypetting import write, comment


class Worklist:
    def __init__(self, experiment, name):
        self.wl_path = experiment.paths["wl"]
        self.wl_file_path = os.path.join(self.wl_path, name)
        self.wl = []

    def add(self, step, msg=False):
        if msg:
            self.wl.append(comment(msg))
        if type(step) == list:
            self.wl += step
        elif type(step) == Worklist:
            self.wl += step.wl
        else:
            self.wl.append(step)

    def save(self):
        write.write_gwl(self.wl_file_path, self.wl)
