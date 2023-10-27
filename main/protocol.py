class Protocol:
    def __init__(self, experiment, name):
        self.filename = name
        self.windows_logfile_path = experiment.windows_paths["log_files"] + "\\" + name
        self.experiment = experiment

    def log_entry(self, message: str):
        time_log_args = {
            "--message": message,
            "--note_path": self.windows_logfile_path
        }
        return self.experiment.execute_command_script("time_log.py", time_log_args)
