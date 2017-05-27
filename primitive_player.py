import asyncio

import pyaudio


class Player:
    playlist = []
    os = None

    def __init__(self, sample_width, channels, rate, ):
        output = pyaudio.PyAudio()
        self.os = output.open(format=output.get_format_from_width(sample_width),
                             channels=channels,
                             rate=rate,
                             output=True)

    def play(self):
        while self.playlist:
            chunck = self.playlist.pop(0)
            # print(chunck)
            self.os.write(chunck)


    def append(self, chunk):
        self.playlist.append(bytes(chunk))
