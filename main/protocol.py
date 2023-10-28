from .base import execute_command_script


class Protocol:
    def __init__(self, logfile_path, windows_python_path):
        self.windows_logfile_path = logfile_path
        self.windows_python_path = windows_python_path

    def log_entry(self, message: str):
        time_log_args = {
            "--message": message,
            "--note_path": self.windows_logfile_path
        }
        return execute_command_script(self.windows_logfile_path, time_log_args, self.windows_python_path)
