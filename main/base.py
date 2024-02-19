import math


def execute_command_script(script_path: str, args: dict, windows_python_path: str):
    cmd = script_path
    for arg, value in args.items():
        cmd += " " + arg + " " + value
    return execute_command_line_python(cmd, windows_python_path)


def execute_command_line_python(command_str: str, windows_python_path: str):
    return direct_command('Execute(' + windows_python_path + " " + command_str+',0,"py_return",2);')


def direct_command(command: str):
    return bytes("B;" + command, "utf-8")


def rrow_to_row(rrow: int, rep: int) -> int:
    return 2 * (rrow - 1) + 1 + int(rep / 2 >= 1)


def rcol_to_col(rcol: int, rep: int) -> int:
    return 2 * rcol - (rep + 1) % 2


def rwell_to_well(rrow: int, rcol: int, rep: int):
    if rep not in [0, 1, 2, 3]:
        raise ValueError("rep must be 0, 1, 2, or 3")
    row = rrow_to_row(rrow, rep)
    col = rcol_to_col(rcol, rep)
    return (row, col)


def well_to_rwell(row:int, col:int):
    rep = 2*int(row / 2 >= 1) + ((col+1) % 2) 
    rrow = math.ceil(row/2)
    rcol = math.ceil(col/2)
    return (rrow, rcol, rep)


def column_mask(rep):
    return 8 * [rep <= 1, rep > 1]

