import math
import struct
from itertools import count, islice

from basic_wave import SineWaveShape
from primitive_player import Player
from sample import MultiWaveBasedSample
from sound_sets import Bauan, Guitar

CHUNK = 10


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


def distorted_sine_wave(frequency=440.0, framerate=44100, amplitude=0.5, dist_base=4, len=None):
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


if __name__ == '__main__':
    time = 2
    sample_width = 2
    frame_rate = 44100
    max_amplitude = float(int((2 ** (sample_width * 8)) / 2) - 1)

    base_fq = 268
    signals_params = [(base_fq, 0.7),
                      (base_fq * 2, 0.3),
                      (base_fq * 3, 0.2),
                      (base_fq * 4, 0.1),
                      (base_fq * 5, 0.2),
                      (base_fq * 6, 0.1),
                      (base_fq * 7, 0.1),
                      (base_fq * 8, 0.1),
                      (base_fq * 9, 0.1),
                      (base_fq * 1.2, 0.2),
                      (base_fq * 1.5, 0.2),
                      ]

    signals_params = normilize(signals_params)
    # print(signals_params)
    signals = [islice(distorted_sine_wave(freq, amplitude=amp, dist_base=10), 0, 44100 * time) for freq, amp in
               signals_params]

    res = combine(*signals)

    samples = list(res)

    packed_samples = [struct.pack('h', int(max_amplitude * sample)) for sample in list(samples)]

    raw_samples = b''.join(packed_samples)

    player = Player(2, 1, frame_rate)

    bauan = Bauan(sample_width, frame_rate)
    guitar = Guitar(sample_width, frame_rate)

    # # player.append(raw_samples)
    # player.append(bauan.generate(268, 2))
    # player.append(bauan.generate(220, 1))
    # player.append(bauan.generate(360, 1))
    #
    # # player.append(raw_samples)
    # player.append(bauan.generate(268, 2))
    # player.append(bauan.generate(220, 1))
    # player.append(bauan.generate(360, 1))
    #
    # player.play()
    #
    # # player.append(raw_samples)
    # player.append(guitar.generate(268, 2))
    # player.append(guitar.generate(220, 1))
    # player.append(guitar.generate(360, 1))
    #
    # player.append(raw_samples)
    # player.append(guitar.generate(268, 2))
    # player.append(guitar.generate(220, 1))
    # player.append(guitar.generate(360, 1))


    # simple_sample = WaveBasedSample(
    #     frequency=256,
    #     amplitude=30,
    #     framerate=44100,
    #     wave_form=SineWaveShape,
    #     length=2,
    #     width=2
    # )
    # distorted_sample = WaveBasedSample(
    #     frequency=256,
    #     amplitude=30,
    #     framerate=44100,
    #     wave_form=DistortedSineWaveShape,
    #     wave_params={'dist_base': 3},
    #     length=2,
    #     width=2
    # )
    #
    # old_octave = [WaveBasedSample(
    #     frequency=fq / 2,
    #     amplitude=20,
    #     framerate=44100,
    #     wave_form=SineWaveShape,
    #     length=1,
    #     width=2
    # ) for fq in [880, 932, 986, 1046, 1108, 1174, 1244, 1318, 1396, 1478, 1568, 1660, 1760]]
    #
    # new_octave = [WaveBasedSample(
    #     frequency=fq / 2,
    #     amplitude=20,
    #     framerate=44100,
    #     wave_form=SineWaveShape,
    #     length=1,
    #     width=2
    # ) for fq in [880, 935, 990, 1045, 1100, 1155, 1265, 1320, 1375, 1485, 1595, 1650, 1760]]
    #
    # new_octave = [WaveBasedSample(
    #     frequency=fq / 2,
    #     amplitude=30,
    #     framerate=44100,
    #     wave_form=SineWaveShape,
    #     length=1,
    #     width=2
    # ) for fq in [880, 935, 990, 1045, 1100, 1155, 1210, 1265, 1320, 1375, 1430, 1485, 1540, 1595, 1650, 1705, 1760]]

    # for chord in combinations(range(12), 3):
    #     set = [old_octave[step] for step in chord]
    #
    #     print(chord)
    #     player.append(set[0] + set[1] + set[2])
    #     player.play()

    # [880, 935, 990, 1045, 1100, 1155, 1210, 1265, 1320, 1375, 1430, 1485, 1540, 1595, 1650, 1705, 1760]
    # [880, 935, 990, 1045, 1100, 1155, 1265, 1320, 1375, 1485, 1595, 1650, 1760]]

    # old_octave = WaveBasedSample(
    #     frequency=256,
    #     amplitude=30,
    #     framerate=44100,
    #     wave_form=SineWave,
    #     length=2,
    #     width=2
    # )

    step = (512 - 256) / 16 * 16

    base = 256
    old_music_step = base / 12
    # mrr_sample = WaveBasedSample(
    #     frequency=base,
    #     amplitude=30,
    #     framerate=44100,
    #     wave_form=SineWaveShape,
    #     # wave_params={'dist_base': 3},
    #     length=10,
    #     width=2
    # )

    # for i in range(17):
    #     print(440 + i * 440 / 16)
    # exit()
    #
    # mrr2_sample = WaveBasedSample(
    #     frequency=base + old_music_step * 0.75,
    #     amplitude=30,
    #     framerate=44100,
    #     wave_form=SineWaveShape,
    #     # wave_params={'dist_base': 3},
    #     length=10,
    #     width=2
    # )

    # mrr3_sample = MultiWaveBasedSample(
    #     frequency=base + old_music_step * 12,
    #     framerate=44100,
    #     waves=[
    #         (1, 80, SineWaveShape, {'dist_base': 3}),
    #         (1.2, 7, SineWaveShape, {'dist_base': 3}),
    #         (1.5, 10, SineWaveShape, {'dist_base': 3}),
    #         (2, 20, SineWaveShape, {'dist_base': 3}),
    #         (3, 3, SineWaveShape, {'dist_base': 3}),
    #         (4, 10, SineWaveShape, {'dist_base': 3}),
    #         (5, 1, SineWaveShape, {'dist_base': 3}),
    #         (6, 5, SineWaveShape, {'dist_base': 3}),
    #         (7, 1, SineWaveShape, {'dist_base': 3}),
    #     ],
    #     sample_amplitude=200,
    #     length=2,
    #     width=2
    # )

    # new_octave_owertones = [MultiWaveBasedSample(
    #     frequency=fq/2,
    #     framerate=44100,
    #     waves=[
    #         (1, 80, SineWaveShape, {'dist_base': 3}),
    #         # (1.2, 7, SineWaveShape, {'dist_base': 3}),
    #         # (1.5, 10, SineWaveShape, {'dist_base': 3}),
    #         (2, 20, SineWaveShape, {'dist_base': 3}),
    #         # (3, 3, SineWaveShape, {'dist_base': 3}),
    #         (4, 10, SineWaveShape, {'dist_base': 3}),
    #         # (5, 1, SineWaveShape, {'dist_base': 3}),
    #         # (6, 5, SineWaveShape, {'dist_base': 3}),
    #         # (7, 1, SineWaveShape, {'dist_base': 3}),
    #     ],
    #     sample_amplitude=200,
    #     length=2,
    #     width=2
    # ) for fq in [880, 935, 990, 1045, 1100, 1155, 1210, 1265, 1320, 1375, 1430, 1485, 1540, 1595, 1650, 1705, 1760]]

    new_octave_owertones = [MultiWaveBasedSample(
        frequency=fq / 4,
        framerate=44100,
        waves=[
            (1, 80, SineWaveShape, {'dist_base': 3}),
            (3 / 2, 15, SineWaveShape, {'dist_base': 3}),
            (4 / 2, 10, SineWaveShape, {'dist_base': 3}),
            (5 / 2, 6, SineWaveShape, {'dist_base': 3}),
            (6 / 2, 4, SineWaveShape, {'dist_base': 3}),
            (7 / 2, 2, SineWaveShape, {'dist_base': 3}),
            (8 / 2, 1, SineWaveShape, {'dist_base': 3}),
            (9 / 2, 1, SineWaveShape, {'dist_base': 3}),
            (7, 1, SineWaveShape, {'dist_base': 3}),
        ],
        sample_amplitude=200,
        length=2,
        width=2
    ) for fq in [880, 935, 990, 1045, 1100, 1155, 1210, 1265, 1320, 1375, 1430, 1485, 1540, 1595, 1650, 1705, 1760]]

    a = 0
    d = 5
    f = 8
    # g c# f

    # player.append(old_octave[a]+ old_octave[d] + old_octave[f])
    #
    # player.append(new_octave_owertones[a]+ new_octave_owertones[d] + new_octave_owertones[f])

    # new = distorted_sample + simple_sample
    # t = SineWaveShape(
    #     frequency=13,
    #     amplitude=20,
    #     framerate=44100
    # )

    # pyplot.plot(range(50_000), list(islice(t, 50_000)))
    # pyplot.plot(range(500), [sin_pure2[i] for i in range(500)], label='dist')
    # pyplot.plot(range(500), [sin_sum[i] for i in range(500)], label='dist')
    # pyplot.plot(range(500), [new[i] for i in range(500)], label='new')
    # pyplot.plot(range(500), [mrr_sample[i] for i in range(500)], label='MRR')
    # pyplot.axes([-50, 44100, 50, 50])
    # pyplot.legend(loc='best')
    # pyplot.show()

    for sample in new_octave_owertones:
        player.append(sample)
    # player.append(distorted_sample+mrr_sample)
    #     player.append(simple_sample + distorted_sample+mrr_sample)
    #     player.append(new)

    player.play()
