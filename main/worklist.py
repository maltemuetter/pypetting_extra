from pypetting import write, comment


class Worklist:
    def __init__(self, filepath, protocol=None, autosave=True):
        self.filepath = filepath
        self.wl = []
        self.protocol = protocol
        self.autosave = autosave

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

        if self.autosave:
            self.save()

    def save(self):
        write.write_gwl(self.filepath, self.wl)

    def add_protocol(self, protocol):
        self.protocol = protocol

    def __repr__(self):
        protocol_info = f"Protocol: {self.protocol}" if self.protocol else "No protocol"
        autosave_status = "enabled" if self.autosave else "disabled"
        return (f"Worklist Filepath: '{self.filepath}'\n"
                f"Steps Count: {len(self.wl)}\n"
                f"{protocol_info}\n"
                f"Autosave: {autosave_status}")
