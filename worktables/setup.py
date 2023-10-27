from pypetting_extra import ROMA, StoreX, LiHA, MCA, Experiment, InfinitePlateReader, Protocol
from mic_setup.hardware_setup import (
    storex_site,
    reader_site,
    pintool_setup,
    ditis_1)
import os
from mic_setup.liquid_classes import minimal_fd, minimal_cd, liha_mix

from pypetting_extra import Worktable


#  Improve
# Worklists
# LIHA Washing steps and devices
#

# Example usage
default_path = "/Users/malte/polybox/Shared/Robot-Malte/pypetting_experiments/"
windows_python_path = "C:\\Users\\COMPUTER\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
windows_base_path = "C:\\Users\\COMPUTER\\polybox\\Robot-Malte\\pypetting"
windows_exp_path = "C:\\Users\\COMPUTER\\polybox\\Robot-Malte\\pypetting_experiments"
timelog_script_path = "\\scripts\\time_log.py"


def initialize(
        exp_name,
        folder_path=default_path,
        windows_python=windows_python_path,
        windows_base=windows_base_path,
        windows_exp=windows_exp_path,
        timelog_script=timelog_script_path):

    experiment = Experiment(
        folder_path,
        exp_name,
        windows_python,
        windows_base,
        windows_exp,
        timelog_script)

    # Liha
    liha = LiHA(minimal_cd, minimal_fd, liha_mix, waste_volume=10)

    # Reader
    od_settings = os.path.join(
        experiment.paths["base"], "mic_setup", "measure.xml")
    lum_settings = os.path.join(
        experiment.paths["base"], "mic_setup", "measure.xml")
    windows_od_files = experiment.paths["windows_exp_path"] + "\\od_files\\"
    od_files = os.path.join(experiment.paths["exp"], "od_files")
    windows_lum_files = experiment.paths["windows_exp_path"] + "\\lum_files\\"
    lum_files = os.path.join(experiment.paths["exp"], "lum_files")
    reader = InfinitePlateReader(reader_site)
    reader.add_settings("od", od_settings, windows_od_files, od_files)
    reader.add_settings("lum", lum_settings, windows_lum_files, lum_files)

    # StoreX
    incubator = StoreX(storex_site)

    # Roma
    roma = ROMA()
    roma.add_incubator(incubator)
    roma.add_plate_reader(reader)

    #  mca
    mca = MCA(ditis_1, extra_vol=8)
    mca.add_pintool_setup(pintool_setup)

    # protocol
    protocol = Protocol(experiment, "log.csv")

    return experiment, reader, roma, liha, mca, protocol
