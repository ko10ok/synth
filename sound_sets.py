import math
import struct
from itertools import islice, count


def combine(*signals, nframes=None):
    res = islice(map(sum, zip(*signals)), nframes)
    return res


def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5, len=None):
    period = len if len else int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [
        float(amplitude) * math.sin(2.0 * math.pi * float(frequency) * (float(i % period) / float(framerate))) for i in
        range(period)]
    return (lookup_table[i % period] for i in count(0))


def distorted_sine_wave(frequency=440.0, framerate=44100, amplitude=0.5, dist_base=2, len=None):
    period = len if len else int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0

    lookup_table = [
        float(amplitude) * math.sin(2.0 * math.pi * float(frequency) * (float(i % period) / float(framerate)))
        / dist_base ** math.fabs(math.sin(2.0 * math.pi * float(frequency) * (float(i % period) / float(framerate))))
        for i in range(period)]
    return (lookup_table[i % period] for i in count(0))


def normilize(*signals_params):
    freqs, amps = zip(*tuple(*signals_params))
    proportion = 1 / sum(amps)
    amps = tuple(amp * proportion for amp in amps)
    return list(zip(freqs, amps))


class Bank():
    signal_form = None

    def __init__(self, sample_width, frame_rate):
        self.sample_width = sample_width
        self.frame_rate = frame_rate
        self.max_amplitude = float(int((2 ** (self.sample_width * 8)) / 2) - 1)

    def generate(self, base_freq, time):
        pass

        frame_rate = 44100
        max_amplitude = float(int((2 ** (self.sample_width * 8)) / 2) - 1)

        signals_params = [(base_freq * mp, amp) for mp, amp in self.signals_params]

        signals_params = normilize(signals_params)
        # print(signals_params)
        signals = [islice(distorted_sine_wave(freq, amplitude=amp, dist_base=10), 0, 44100 * time) for freq, amp in
                   signals_params]

        res = combine(*signals)

        samples = list(res)

        packed_samples = [struct.pack('h', int(max_amplitude * sample)) for sample in list(samples)]

        raw_samples = b''.join(packed_samples)

        return raw_samples


class Bauan(Bank):
    signal_form = distorted_sine_wave
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
