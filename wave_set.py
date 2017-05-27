from sample import Sample


class WaveSet(list):
    signal_form = None

    def __init__(self):
        super().__init__()
        self.extend(self.signals_params)




class Bauan(Bank):
    signals_params = [(1, 0.7),
                      (2, 0.3),
                      (3, 0.2),
                      (4, 0.1),
                      (5, 0.2),
                      (6, 0.1),
                      (7, 0.1),
                      (8, 0.1),
                      (9, 0.1),
                      (1.2, 0.2),
                      (1.5, 0.2)]


class Guitar(Bank):
    signals_params = [(1, 1)]
