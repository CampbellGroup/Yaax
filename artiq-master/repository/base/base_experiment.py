from artiq.experiment import Experiment



class YaaxExperiment(Experiment):
       
        def build(self):
            super().build()

        def prepare(self):
            delattr(Experiment, "prepare")
            super().prepare()