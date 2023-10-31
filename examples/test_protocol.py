from pypetting_extra.custom_scripts.routines import make_photos_of_plates
from pypetting_extra import robot, Plate, Experiment, Protocol
from pypetting import Labware
from pypetting_extra.main.base import direct_command
import os

exp_path = "/Users/malte/polybox/Shared/Robot-Malte/test_folder"
experiment = Experiment(
    "test", exp_path, "C:\\Users\\COMPUTER\\polybox\\Robot-Malte\\test_folder")
experiment.initialize()
protocol = experiment.setup_protocol()
wl = experiment.setup_worklist("test.gwl", protocol)
wl.add(protocol.log_entry("bli_bla_blubb"))
wl.save()
