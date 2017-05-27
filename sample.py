import operator
import struct
from functools import reduce
from itertools import islice, starmap, zip_longest

from basic_wave import WaveShape


class Sample(list):
    def __init__(self, framerate, length, width):
        super().__init__()
        self.framerate = framerate
        self.length = length
        self.width = width
        self.sample_amplitude = 100

    def _normalized(self):
        max_amplitude = float(int((2 ** (self.width * 8)) / 2) - 1)
        normalized_sample = [float(x) / self.sample_amplitude * max_amplitude for x in self]

        return normalized_sample

    def __and__(self, other):
        min_len = min(len(self), len(other))
        max_len = min(len(self), len(other))

        new_sample = Sample(self.framerate, self.length, self.width)
        new_sample.sample_amplitude = 100
        new_sample.extend(starmap(lambda x, y: max(min(self.sample_amplitude, x + y), -self.sample_amplitude),
                                  zip_longest(self, other, fillvalue=0)))
        return new_sample

    def __add__(self, other):
        min_len = min(len(self), len(other))
        max_len = min(len(self), len(other))

        new_sample = Sample(self.framerate, self.length, self.width)
        new_sample.sample_amplitude = self.sample_amplitude + other.sample_amplitude
        new_sample.extend(starmap(lambda x, y: max(min(self.sample_amplitude, x + y), -self.sample_amplitude),
                                  zip_longest(self, other, fillvalue=0)))
        return new_sample

    def is_overdriven(self):
        if (self.sample_amplitude in self or -self.sample_amplitude in self):
            return True
        else:
            return False

    def __str__(self):
        packed_samples = [struct.pack('h', int(sample)) for sample in self._normalized()]
        raw_samples = b''.join(packed_samples)
        return str(raw_samples)

    def __bytes__(self):
        packed_samples = [struct.pack('h', int(sample)) for sample in self._normalized()]
        raw_samples = b''.join(packed_samples)
        return raw_samples

    def trim_ends(self, wave: WaveShape, lengh):
        pass

class WaveBasedSample(Sample):
    def __init__(self, frequency: float,
                 amplitude: float,
                 framerate: float,
                 width: float,
                 wave_form: WaveShape.__class__,
                 length: float,
                 wave_params=None,
                 sample_amplitude=100):

        super().__init__(framerate, length, width)
        self.framerate = framerate
        self.length = length
        self.sample_amplitude = sample_amplitude
        self.extend(islice(wave_form(frequency, amplitude, framerate, wave_params), int(length * framerate)))


class MultiWaveBasedSample(Sample):
    def __init__(self,
                 frequency: float,
                 framerate: float,
                 width: float,
                 length: float,
                 waves: list,
                 sample_amplitude: float = None):
        super().__init__(framerate, length, width)
        self.framerate = framerate
        self.length = length
        self.sample_amplitude = sample_amplitude if sample_amplitude else sum([amp for stp, amp, wf, wp in waves])
        [print(frequency*stp) for stp, amp, wf, wp in waves]
        self.extend(
            reduce(
                operator.add,
                [
                    WaveBasedSample((frequency * step), amp, framerate, width, wave_form, length, wave_params,
                                    amp)
                    for step, amp, wave_form, wave_params in waves
                ]
            )
        )
