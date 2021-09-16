from functools import partial
from threading import Thread
from time import sleep

import numpy as np
import zmq
from tornado import gen

from STFT import STFT


class STFTReceiver(Thread):
    def __init__(self, document, source, spectrogram, signaler, context, endpoint):
        super().__init__()
        self.document = document
        self.source = source
        self.spectrogram = spectrogram
        self.signaler = signaler
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe("")
        self.count_between_renders = 20

    def run(self):
        while not self.signaler.should_shutdown():
            frames_collected = 0
            while frames_collected < self.count_between_renders:
                envelope = self.socket.recv_multipart()
                new_stft = STFT.GetRootAsSTFT(envelope[1], 0)
                self.spectrogram = self.spectrogram[:-1, :]
                magnitudes = new_stft.MagnitudesAsNumpy()
                magnitudes = np.expand_dims(magnitudes, axis=0)
                self.spectrogram = np.concatenate((magnitudes, self.spectrogram))
                frames_collected += 1
            self.document.add_next_tick_callback(partial(update, source=self.source, spectrogram=self.spectrogram))


@gen.coroutine
def update(source, spectrogram):
    new_data = {
        "image": [spectrogram.T]
    }
    source.stream(new_data, rollover=1)
