from .base import execute_command_script


class Protocol:
    def __init__(self, cmd_script_path, logfile_path, windows_python_path):
        self.cmd_script_path = cmd_script_path
        self.windows_logfile_path = logfile_path
        self.windows_python_path = windows_python_path

    def log_entry(self, message: str):
        time_log_args = {
            "--message": message,
            "--note_path": self.windows_logfile_path
        }
        self.check_for_blank(message)
        return execute_command_script(self.cmd_script_path, time_log_args, self.windows_python_path)

    def check_for_blank(self, message):
        if len(message.split(" ")) > 1:
            raise Exception("message cannot contain blanks. Use '_' instead")
