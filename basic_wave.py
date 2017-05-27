import math


class WaveShape():
    def __init__(self, frequency: float, amplitude: float, framerate: float):
        self.period = int(float(framerate) / float(frequency))
        self.amplitude = amplitude
        self.frequency = frequency
        self.framerate = framerate

    def __getitem__(self, item):
        return (self.lookup_table[item % self.period])

    def __call__(self, *args, **kwargs):
        i, = args
        return (self.lookup_table[int(i) % self.period])


class SineWaveShape(WaveShape):
    def __init__(self, frequency, amplitude, framerate, wave_params=None):
        super().__init__(frequency, amplitude, framerate)
        self.lookup_table = [float(amplitude) * math.sin(
            2.0 * math.pi * float(frequency) * (float(i % self.period) / float(framerate))
        ) for i in range(self.period)]


class DistortedSineWaveShape(WaveShape):
    def __init__(self, frequency, amplitude, framerate, wave_params=None):
        super().__init__(frequency, amplitude, framerate)

        self.lookup_table = [
            float(amplitude) * math.sin(
                2.0 * math.pi * float(frequency) * (float(i % self.period) / float(framerate))
            ) / ((wave_params.get('dist_base') ** math.fabs(math.sin(
                2.0 * math.pi * float(frequency) * (float(i % self.period) / float(framerate))
            ))) if wave_params else 1)
            for i in range(self.period)
        ]
