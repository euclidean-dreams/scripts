from threading import Thread

import zmq

from ImpresarioSerialization.Onset import Onset
from dev_dashboard.utils import get_onset_method_string_from_number


class OnsetReceiver(Thread):
    def __init__(self, signaler, context, endpoint):
        super().__init__()
        self.flip = True
        self.signaler = signaler
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe("")

    def run(self):
        while not self.signaler.should_shutdown():
            onset = self.receive_onset()
            if self.flip:
                extra = "+"
            else:
                extra = "-"
            print(f"{get_onset_method_string_from_number(onset.Method())} {extra}")
            self.flip = not self.flip

    def receive_onset(self):
        envelope = self.socket.recv_multipart()
        return Onset.GetRootAsOnset(envelope[0], 0)
