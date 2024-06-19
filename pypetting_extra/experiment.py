import os
from .base import direct_command
import shutil
from .worklist import Worklist
from .protocol import Protocol
from .platereader import Measurement
from .location import Location
import pandas as pd


class Experiment:
    def __init__(
        self,
        exp_name,
        mac_experiment_folder_path,
        windows_experiment_folder_path,
        windows_python_path="C:\\Users\\COMPUTER\\AppData\\Local\\Programs\\Python\\Python310\\python.exe",
        clone_src=True,
    ):

        self.path = mac_experiment_folder_path
        self.windows_path = windows_experiment_folder_path
        self.windows_paths = {"python": windows_python_path}
        self.name = exp_name

        self.folders = {
            "exp": [exp_name],
            "notes": [exp_name, "notes"],
            "wl": [exp_name, "worklists"],
        }

        self.make_paths()
        self.make_windows_paths()
        self.write_folders()
        if clone_src:
            self.clone_src_code()

    def add_folder(self, key, folder, write=True):
        self.folders.update({key: [self.name, folder]})
        if write:
            self.make_paths()
            self.make_windows_paths()
            self.write_folders()

    def write_variable_txt(self, name, value, folderkey="evoscripts"):
        path = os.path.join(self.paths[folderkey], name + ".txt")
        with open(path, "w") as file:
            file.write(str(value))

    def del_folder(self, key):
        if key in self.folders:
            del self.folders[key]

    def make_paths(self):
        self.paths = {}
        for key, folder in self.folders.items():
            self.paths.update({key: os.sep.join([self.path] + folder)})

    def make_windows_paths(self):
        for key, folder in self.folders.items():
            self.windows_paths.update({key: "\\".join([self.windows_path] + folder)})

    def write_folders(self):
        for path in self.paths.values():
            if not os.path.exists(path):
                os.makedirs(path)

    def execute_command_script(self, script_name, args: dict):
        script_path = self.windows_paths["cmd_scripts"] + "\\" + script_name
        cmd = script_path
        for arg, value in args.items():
            cmd += ' "' + arg + '" ' + value
        return self.execute_command_line_python(cmd)

    def execute_command_line_python(self, command_str: str):
        return direct_command(
            "Execute("
            + self.windows_paths["python"]
            + " "
            + command_str
            + ',0,"py_return",2);'
        )

    def setup_worklist(self, name, protocol=None):
        return Worklist(os.path.join(self.paths["wl"], name), protocol=protocol)

    def setup_pickolo_folder(self, folder_key, folder_name, liha):
        self.add_folder(folder_key, folder_name, write=True)
        liha.pickolo.set_img_folder(self.windows_paths[folder_key])

    def setup_protocol(self, script_name="time_log.py", file_name="timelog.csv"):
        logfile_path = self.windows_paths["notes"] + "\\" + file_name
        script_path = self.windows_paths["cmd_scripts"] + "\\" + script_name
        return Protocol(script_path, logfile_path, self.windows_paths["python"])

    def setup_measurement(self, settings_file_name, folder_key):
        if folder_key not in self.paths.keys():
            self.add_folder(folder_key, folder_key, write=True)

        settings_path = os.path.join(self.paths["reader_settings"], settings_file_name)
        output_folder = self.windows_paths[folder_key]
        return Measurement(settings_path, output_folder)

    def setup_location_file(self, folderkey="notes", filename="locations.csv"):
        filepath = os.path.join(self.paths[folderkey], filename)
        return Location(filepath)

    def save_csv(self, df: pd.DataFrame, filename, folder="notes"):
        filepath = os.path.join(self.paths[folder], filename)
        df.to_csv(filepath, index=False)

    def clone_folder(self, foldername: str):
        src_folder_path = os.path.join(os.getcwd(), foldername)
        dest_folder_path = os.path.join(self.path, self.name, foldername)
        os.makedirs(dest_folder_path, exist_ok=True)

        for filename in os.listdir(src_folder_path):
            src_file_path = os.path.join(src_folder_path, filename)
            dest_file_path = os.path.join(dest_folder_path, filename)

            if os.path.isfile(src_file_path) and not os.path.exists(dest_file_path):
                shutil.copy(src_file_path, dest_file_path)

        self.add_folder(foldername, foldername)

    def clone_src_code(
        self, extensions: list = [".py", ".xlsx", ".md", ".rmd", ".txt"]
    ):
        src_folder_path = os.getcwd()
        dest_folder_path = os.path.join(self.path, self.name, "src_code")
        os.makedirs(dest_folder_path, exist_ok=True)

        for filename in os.listdir(src_folder_path):
            if filename.startswith("~$"):
                continue
            if any(filename.endswith(ext) for ext in extensions):
                src_file_path = os.path.join(src_folder_path, filename)
                dest_file_path = os.path.join(dest_folder_path, filename)

                if os.path.isfile(src_file_path) and not os.path.exists(dest_file_path):
                    shutil.copy(src_file_path, dest_file_path)

        self.add_folder("src_code", "src_code")

    def make_path_file(self):
        file_path = os.path.join(self.paths.get("evoscripts"), "path.txt")
        with open(file_path, "w") as file:
            file.write(self.windows_paths["exp"] + "\\")
