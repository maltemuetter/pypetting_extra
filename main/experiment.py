import os
from .base import direct_command
from pypetting import write
import shutil
from .worklist import Worklist
from .protocol import Protocol
from .platereader import Measurement


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
            "wl": [exp_name, "worklists"],
            "reader_settings": [exp_name, "reader_settings"]
        }

    def initialize(self, copy_cmd_scripts=True, copy_reader_settings=True):
        self.make_paths()
        self.make_windows_paths()
        self.write_folders()
        if copy_cmd_scripts:
            self.clone_command_scripts()
        if copy_reader_settings:
            self.clone_reader_settings()

    def add_folder(self, key, folder):
        self.folders.update({key: folder})

    def replace_folders(self, folders):
        self.folders = folders

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

    def clone_reader_settings(self):
        import pypetting_extra.reader_settings as reader_settings
        reader_settings_path = reader_settings.__path__[0]
        for filename in os.listdir(reader_settings_path):
            if filename.endswith(".xml"):
                src_path = os.path.join(reader_settings_path, filename)
                dest_path = os.path.join(
                    self.paths["reader_settings"], filename)
                shutil.copy(src_path, dest_path)

    def execute_command_script(self, script_name, args: dict):
        script_path = self.windows_paths["cmd_scripts"] + "\\" + script_name
        cmd = script_path
        for arg, value in args.items():
            cmd += ' "' + arg + '" ' + value
        return self.execute_command_line_python(cmd)

    def execute_command_line_python(self, command_str: str):
        return direct_command('Execute(' + self.windows_paths["python"] + " " + command_str+',0,"py_return",2);')

    def setup_worklist(self, name, protocol=None):
        return Worklist(os.path.join(self.paths["wl"], name), protocol=protocol)

    def setup_protocol(self, name="timelog.csv"):
        logfile_path = self.windows_paths["log_files"] + "\\" + name
        return Protocol(logfile_path, self.windows_paths["python"])

    def setup_measurement(self, settings_file_name, folder_key):
        settings_path = os.path.join(
            self.paths["reader_settings"], settings_file_name)
        output_folder = self.windows_paths[folder_key]
        return Measurement(settings_path, output_folder)
