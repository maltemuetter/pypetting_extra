from pypetting import open_infinite_reader, close_infinite_reader, measure_infinite_reader


class InfinitePlateReader:
    def __init__(self, gridsite, settings_folder_path=None):
        self.gridsite = gridsite
        self.is_open = False
        self.settings_folder = settings_folder_path

    def add_settings_folder(self, path):
        self.settings_folder = path

    def open(self):
        self.is_open = True
        return open_infinite_reader()

    def close(self):
        self.is_open = False
        return close_infinite_reader()

    def measure(self, file_path, settings_file_name):
        settings_path = self.settings_folder + settings_file_name
        return measure_infinite_reader(file_path, settings_path)

    def return_measurement_method(self, settings_file_name, output_folder_path):
        settings_path = self.settings_folder + "\\" + settings_file_name
        return Measurement(settings_path, output_folder_path)


class Measurement:
    def __init__(self, settings_path, output_folder_path):
        self.settings = settings_path
        self.output = output_folder_path

    def measure(self, filename):
        file_path = self.output + "\\" + filename
        return measure_infinite_reader(file_path, self.settings)
