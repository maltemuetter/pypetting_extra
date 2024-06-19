from pypetting_extra import default_worktable, Experiment
from pypetting.labware import labwares
from pypetting import Labware


mp3pos = default_worktable.carrier["MP 3Pos Fixed"]
liha = default_worktable.liha
pbs_trough = default_worktable.carrier["MP 3Pos Deck"].define_plate(
    "PBS", Labware("Trough 300ml MCA", 8, 12), 2
)

folder = "test_pypetting_extra"
exp_path = "/Users/malte/polybox/Shared/Robot-Shared/" + folder
experiment = Experiment(
    "test",
    exp_path,
    "C:\\Users\\COMPUTER\\polybox\\Robot-Shared\\" + folder,
)


fill_volume = 100
plate96 = mp3pos.define_plate("test_plate", labwares["greiner96"], 1)

wl = experiment.setup_worklist("test_liha.gwl")
wl.add(
    liha.fill_96_well_plate(
        pbs_trough,
        plate96,
        fill_volume,
        8 * [True],
        start_col=1,
        end_col=10,
        liquid_class="Minimal FD mix",
    )
)
