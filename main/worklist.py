import os
from pypetting import write, comment


class Worklist:
    def __init__(self, filepath, protocol=None):
        self.wl_file_path = filepath
        self.wl = []
        self.protocol = protocol

    def add(self, step, msg=False):
        if msg:
            self.wl.append(comment(msg))
            if self.protocol:
                self.wl += [self.protocol.log_entry(msg)]
        if type(step) == list:
            self.wl += step
        elif type(step) == Worklist:
            self.wl += step.wl
        else:
            self.wl.append(step)

    def save(self):
        write.write_gwl(self.wl_file_path, self.wl)

    def add_protocol(self, protocol):
        self.protocol = protocol
