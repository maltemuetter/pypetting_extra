import os
from .base import direct_command
from pypetting import write


class Experiment:
    def __init__(self,
                 folder_path,
                 exp_name,
                 windows_python_path,
                 windows_base_path,
                 windows_exp_path,
                 timelog_script_path):

        # make paths
        self.name = exp_name
        self.paths = {
            "exp": os.path.join(folder_path, exp_name),
            "windows_base": windows_base_path,
            "base": os.path.join(os.getcwd()),
            "windows_python": windows_python_path,
            "windows_exp_path": windows_exp_path + "\\" + exp_name,
            "windows_log_files": windows_exp_path + "\\" + exp_name + "\\" + "log_files",
            "timelog_script": windows_base_path+timelog_script_path}

        self.make_exp_folders()

    def make_exp_folders(self):
        exp_path = self.paths["exp"]
        self.exp_folders = {"exp": exp_path,
                            "obj": os.path.join(exp_path, "obj"),
                            "wl": os.path.join(exp_path, "worklists"),
                            "log": os.path.join(exp_path, "log_files")}
        self.create_folders()
        self.paths.update(self.exp_folders)

    def create_folders(self):
        for path in self.exp_folders.values():
            self.create_folder(path)

    def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def add_path(self, key, path, folder=True):
        self.paths.update({key: path})
        if folder:
            self.exp_folders.update({key: path})
            self.create_folder(path)

    def execute_command_line_python(self, command_str: str):
        return direct_command('Execute(' + self.paths["windows_python"] + " " + command_str+',0,"py_return",2);')

    def save_wl(self, wl: list, name: str):
        write.write_gwl(os.path.join(
            self.paths["wl"], name), wl)
