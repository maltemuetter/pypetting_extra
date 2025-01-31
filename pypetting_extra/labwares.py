from pypetting import Labware

labwares = {
    "trough100": Labware(name="Trough 100+25ml", rows=8, cols=1, spacing=1),
    "greiner96": Labware(name="96 Well Greiner SC", rows=8, cols=12, spacing=1),
    "greiner384": Labware(name="384 Well Plate Greiner", rows=16, cols=24, spacing=2),
    "corning8row": Labware("8 Row DeepWell Corning", 8, 1),
    "deepwell96": Labware("96 DeepWell Greiner", 8, 12),
    "trough300": Labware("Trough 300ml MCA", 8, 12),
}
