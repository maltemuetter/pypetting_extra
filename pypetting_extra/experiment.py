import os
from .base import direct_command
import shutil
from .worklist import Worklist
from .protocol import Protocol
from .platereader import Measurement
from .location import Location
import pandas as pd
import sys


class Experiment:
    def __init__(
        self,
        exp_name,
        mac_experiment_folder_path,
        windows_experiment_folder_path,
        windows_python_path="C:\\Users\\COMPUTER\\AppData\\Local\\Programs\\Python\\Python310\\python.exe",
        clone_src=True,
        default_folders=["notes", "worklists"],
        default_keys=["notes", "wl"],
    ):

        self.check_overwrite(mac_experiment_folder_path, exp_name)
        self.path = mac_experiment_folder_path
        self.windows_path = windows_experiment_folder_path
        self.windows_paths = {"python": windows_python_path}
        self.name = exp_name

        # mk base folder
        self.folders = {
            "exp": [exp_name],
        }
        self.make_paths()
        self.make_windows_paths()
        self.write_folders()

        # mk sub folders
        for folder, key in zip(default_folders, default_keys):
            self.add_folder(key, folder, write=False)

        if clone_src:
            self.clone_src_code()

    @staticmethod
    def check_overwrite(mac_experiment_folder_path, exp_name):
        if os.path.exists(os.path.join(mac_experiment_folder_path, exp_name)):
            overwrite = input(
                f"The experiment folder {mac_experiment_folder_path} already exists. Do you want to overwrite it? (yes/no): "
            )
            if overwrite.lower() != "yes":
                print("Operation aborted.")
                sys.exit()

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

    def setup_worklist(self, name, protocol=None, folder_name="worklists", key="wl"):
        if not self.exist(folder_name):
            print(f"folder {folder_name} newly created")
            self.add_folder(key, folder_name)
        return Worklist(os.path.join(self.paths[key], name), protocol=protocol)

    def setup_pickolo_folder(self, folder_key, folder_name, liha):
        self.add_folder(folder_key, folder_name, write=True)
        liha.pickolo.set_img_folder(self.windows_paths[folder_key])

    def setup_protocol(
        self, script_name="time_log.py", file_name="timelog.csv", folder_key="notes"
    ):
        logfile_path = self.windows_paths[folder_key] + "\\" + file_name
        script_path = self.windows_paths["cmd_scripts"] + "\\" + script_name
        return Protocol(script_path, logfile_path, self.windows_paths["python"])

    def setup_measurement(
        self, settings_file_name, folder_key, xml_folder="reader_settings"
    ):
        if folder_key not in self.paths.keys():
            self.add_folder(folder_key, folder_key, write=True)

        settings_path = os.path.join(self.paths[xml_folder], settings_file_name)
        output_folder = self.windows_paths[folder_key]
        return Measurement(settings_path, output_folder)

    def setup_location_file(self, folderkey="notes", filename="locations.csv"):
        filepath = os.path.join(self.paths[folderkey], filename)
        return Location(filepath)

    def save_csv(self, df: pd.DataFrame, filename, folder_key="notes"):
        filepath = os.path.join(self.paths[folder_key], filename)
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

    def exist(self, folder, path=None):
        if not path:
            path = self.paths["exp"]
        return os.path.exists(os.path.join(path, folder))
