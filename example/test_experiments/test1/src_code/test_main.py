from pypetting_extra import Experiment
from pypetting_extra import default_worktable as worktable
from pypetting.labware import labwares
import os

# Soft Setup
folder = "test_experiments"
exp_name = "test1"
exp_path = os.path.join(os.getcwd(), folder)
experiment = Experiment(
    exp_name,
    exp_path,
    "C:\\Users\\COMPUTER\\polybox\\Robot-Malte\\Luminescence\\" + folder,
)

exp_path = os.path.join(os.getcwd(), "test")
experiment = Experiment(
    "test_exp", exp_path, "C:\\Users\\COMPUTER\\polybox\\Robot-Malte\\test"
)
experiment.clone_folder("cmd_scripts")
protocol = experiment.setup_protocol("time_log.py")


# Hard Setup
shelf = worktable.carrier["Shelf 8x4Pos"]
mp2 = worktable.carrier["MP 2Pos Fixed"]
dilution_plate = shelf.define_plate(
    "dilution_plate", labwares["greiner96"], 31, is_store_pos=True
)
plate_pos1 = mp2.gridsite(0)
roma = worktable.roma
liha = worktable.liha

# Generate Worklist
wl = experiment.setup_worklist("test_script.gwl", protocol=protocol)
wl.add(
    roma.move_plate(
        dilution_plate,
        plate_pos1,
        end_with_covered_plate=False,
        new_lid_gridsite=dilution_plate.gridsite,
    ),
    msg="moved_dilution_plate",
)
wl.add(liha.aspirate(dilution_plate, 1, 10, 8 * [True]))
wl.add(liha.dispense(dilution_plate, 2, 10, 8 * [True]), msg="transferred_medium")
wl.add(roma.store(dilution_plate))
