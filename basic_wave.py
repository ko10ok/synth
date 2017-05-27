import math
from itertools import cycle


class WaveShape:
    def __init__(self, lookup_table):
        self.lookup_table = lookup_table

    def __iter__(self):
        return cycle(self.lookup_table)

    @DeprecationWarning
    def __getitem__(self, item):
        return self.lookup_table[item % self.period]


class SineWaveShape(WaveShape):
    def __init__(self, frequency, amplitude, framerate, wave_params=None):
        period = int(float(framerate) / float(frequency))
        lookup_table = [float(amplitude) * math.sin(
            2.0 * math.pi * float(frequency) * (float(i % period) / float(framerate))
        ) for i in range(period)]
        super().__init__(lookup_table)
        self.period = period


class DistortedSineWaveShape(WaveShape):
    def __init__(self, frequency, amplitude, framerate, wave_params=None):
        period = int(float(framerate) / float(frequency))
        lookup_table = [
            float(amplitude) * math.sin(
                2.0 * math.pi * float(frequency) * (float(i % period) / float(framerate))
            ) / ((wave_params.get('dist_base') ** math.fabs(math.sin(
                2.0 * math.pi * float(frequency) * (float(i % period) / float(framerate))
            ))) if wave_params else 1)
            for i in range(period)
        ]
        super().__init__(lookup_table)
        self.period = period
