from pypetting_extra import robot, Experiment

exp_path = os.path.join(os.getcwd(), "experiments")
exp_name = "test"
experiment = Experiment(
    exp_name, exp_path, "C:\\Users\\COMPUTER\\polybox\\Robot-Malte")
experiment.replace_folders({"wl": [exp_name, "worklists"]})
experiment.initialize(copy_cmd_scripts=False)

worklist = experiment.make_worklist("tilter.gwl")


tilter = robot.tilter
worklist.add(tilter.tilt())
worklist.save()
