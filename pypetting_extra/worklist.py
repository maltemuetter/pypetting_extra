from pypetting import write, comment, user_prompt
import os


class Worklist:
    def __init__(self, filepath, protocol=None, autosave=True, initial_comment=True):
        self.filepath = filepath
        self.wl_name = os.path.split(filepath)[-1]
        self.wl = []
        self.protocol = protocol
        self.autosave = autosave
        if initial_comment:
            self.add_msg("Execute:" + self.wl_name)

    def add_msg(self, msg):
        self.wl.append(comment(msg))
        if self.protocol:
            self.wl += [self.protocol.log_entry(msg)]

    def add(self, step, msg=False):
        if msg:
            self.add_msg(msg)

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

    def user_prompt(self, msg):
        self.add_msg(msg)
        self.wl.append(user_prompt(msg))

    def __repr__(self):
        protocol_info = f"Protocol: {self.protocol}" if self.protocol else "No protocol"
        autosave_status = "enabled" if self.autosave else "disabled"
        return (
            f"Worklist Filepath: '{self.filepath}'\n"
            f"Steps Count: {len(self.wl)}\n"
            f"{protocol_info}\n"
            f"Autosave: {autosave_status}"
        )
