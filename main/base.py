def execute_command_script(script_path: str, args: dict, windows_python_path: str):
    cmd = script_path
    for arg, value in args.items():
        cmd += " " + arg + " " + value
    return execute_command_line_python(cmd, windows_python_path)


def execute_command_line_python(command_str: str, windows_python_path: str):
    return direct_command('Execute(' + windows_python_path + " " + command_str+',0,"py_return",2);')


def direct_command(command: str):
    return bytes("B;" + command, "utf-8")
