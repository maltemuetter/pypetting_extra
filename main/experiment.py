import os
from .base import direct_command
from pypetting import write
import shutil


class Experiment:
    def __init__(self,
                 exp_name,
                 mac_experiment_folder_path,
                 windows_experiment_folder_path,
                 windows_python_path="C:\\Users\\COMPUTER\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"):

        self.path = mac_experiment_folder_path
        self.windows_path = windows_experiment_folder_path
        self.windows_paths = {"python": windows_python_path}
        self.name = exp_name

        self.folders = {
            "exp": [exp_name],
            "log_files": [exp_name, "log_files"],
            "cmd_scripts": [exp_name, "cmd_scripts"],
            "img": [exp_name, "img_files"],
            "lum": [exp_name, "lum_files"],
        }

    def initialize(self):
        self.make_paths()
        self.make_windows_paths()
        self.write_folders()
        self.clone_command_scripts()

    def add_folder(self, key, folder):
        self.folders.update({key: folder})

    def del_folder(self, key):
        if key in self.folders:
            del self.folders[key]

    def make_paths(self):
        self.paths = {}
        for key, folder in self.folders.items():
            self.paths.update({key: os.sep.join([self.path] + folder)})

    def make_windows_paths(self):
        for key, folder in self.folders.items():
            self.windows_paths.update(
                {key: "\\".join([self.windows_path] + folder)})

    def write_folders(self):
        for path in self.paths.values():
            if not os.path.exists(path):
                os.makedirs(path)

    def clone_command_scripts(self):
        import pypetting_extra.cmd_scripts as cmd
        cmd_path = cmd.__path__[0]
        for filename in os.listdir(cmd_path):
            if filename.endswith(".py"):
                src_path = os.path.join(cmd_path, filename)
                dest_path = os.path.join(self.paths["cmd_scripts"], filename)
                shutil.copy(src_path, dest_path)

    def execute_command_script(self, script_name, args: dict):
        script_path = self.windows_paths["cmd_scripts"] + "\\" + script_name
        cmd = script_path
        for arg, value in args.items():
            cmd += ' "' + arg + '" ' + value
        return self.execute_command_line_python(cmd)

    def execute_command_line_python(self, command_str: str):
        return direct_command('Execute(' + self.windows_paths["python"] + " " + command_str+',0,"py_return",2);')
