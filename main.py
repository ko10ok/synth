import operator
from functools import reduce
from time import sleep

from pygame import midi

from basic_wave import SineWaveShape
from primitive_player import Player
from sample import MultiWaveBasedSample

if __name__ == '__main__':
    # деленный на 16 частей
    note_set = [880, 935, 990, 1045, 1100, 1155, 1210, 1265, 1320, 1375, 1430, 1485, 1540, 1595, 1650, 1705, 1760]

    # приближение к равномернотемперированному гармоник
    note_set = [880, 935, 990, 1045, 1100, 1155, 1265, 1320, 1375, 1485, 1595, 1650, 1760]

    # гармоники
    note_set = [880, 935, 990, 1045, 1100, 1155, 1210, 1265, 1320, 1375, 1430, 1485, 1540, 1595, 1650, 1705, 1760]

    # гармоники на октаву ниже
    # note_set = [440, 467.5, 495, 522.5, 550, 577.5, 605, 632.5, 660, 687.5, 715, 742.5, 770, 797.5, 825, 852.5]

    # равномерно темперированный
    # note_set = [880, 932, 986, 1046, 1108, 1174, 1244, 1318, 1396, 1478, 1568, 1660, 1760]

    new_octave = [MultiWaveBasedSample(
        frequency=fq / 4,
        framerate=44100,
        waves=[
            (1, 80, SineWaveShape, {'dist_base': 3}),
            (3 / 2, 15, SineWaveShape, {'dist_base': 3}),
            (4 / 2, 10, SineWaveShape, {'dist_base': 3}),
            (5 / 2, 6, SineWaveShape, {'dist_base': 3}),
            (6 / 2, 4, SineWaveShape, {'dist_base': 3}),
            (7 / 2, 2, SineWaveShape, {'dist_base': 3}),
        ],
        sample_amplitude=200,
        length=0.5,
        width=2
    ) for fq in note_set]

    sample_width = 2
    frame_rate = 44100
    player = Player(sample_width, 1, frame_rate)

    midi.init()
    id = midi.get_default_input_id()
    #mkeys = midi.Input(id)
    keys = [20,56,89]
    while True:
        # if mkeys.poll():
        #     sleep(0.2)
            # queue = mkeys.read(20)
            # print(queue)
            # [keys.append(x[0][1]) for x in queue if x[0][2] is not 0 and x[0][1] not in keys]
            # [keys.remove(x[0][1]) for x in queue if x[0][2] is 0 and x[0][1] in keys]
        if len(keys) > 0:
            player.append(reduce(operator.add, [new_octave[key % len(note_set)] for key in keys]))
        player.play()
