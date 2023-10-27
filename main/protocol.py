
class Protocol:
    def __init__(self, experiment, name):
        self.paths = experiment.paths
        self.windows_folder_path = experiment.paths["windows_log_files"]
        self.windows_script_path = experiment.paths["timelog_script"]
        self.filename = name
        self.windows_file_path = self.windows_folder_path + "\\" + name
        self.experiment = experiment

    def log_entry(self, message: str):
        cmd = self.windows_script_path + " --message " + '"' + \
            message + '"' + " --note_path " + self.windows_file_path
        return self.experiment.execute_command_line_python(cmd)
