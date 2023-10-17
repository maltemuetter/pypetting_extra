import os
from pypetting import open_infinite_reader, close_infinite_reader, measure_infinite_reader


class InfinitePlateReader:
    def __init__(self, position):
        self.position = position
        self.is_open = False
        self.settings = {}
        self.folder_paths = {}

    def open(self):
        self.is_open = True
        return open_infinite_reader()

    def close(self):
        self.is_open = False
        return close_infinite_reader()

    def measure(self, file_name, settings_key):
        settings_path = self.settings[settings_key]
        file_path = self.folder_paths[settings_key] + file_name
        return measure_infinite_reader(file_path, settings_path)

    def add_settings(self, key, settings_file_path, windows_folder_path, mac_folder_path):
        self.settings.update({key: settings_file_path})
        self.folder_paths.update({key: windows_folder_path})
        self.create_folder(mac_folder_path)

    def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
