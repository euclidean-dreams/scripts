import time
from threading import Thread

import zmq

from ImpresarioSerialization.AudioAttributes import AudioAttributes
from dev_dashboard.utils import get_onset_method_string_from_number, get_onset_method_names


class AudioAttributesReceiver(Thread):
    def __init__(self, signaler, context, endpoint):
        super().__init__()
        self.signaler = signaler
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe("")
        self.onset_method_names = get_onset_method_names()

    def run(self):
        while not self.signaler.should_shutdown():
            attributes = self.receive_audio_attributes()
            self.print_audio_attributes(attributes)

    def receive_audio_attributes(self):
        envelope = self.socket.recv_multipart()
        return AudioAttributes.GetRootAsAudioAttributes(envelope[0], 0)

    def print_audio_attributes(self, attributes):
        raw_onsets = attributes.OnsetAggregate()
        onsets = {}
        for i in range(raw_onsets.TimestampsLength()):
            onset_name = get_onset_method_string_from_number(raw_onsets.Methods(i))
            onsets[onset_name] = raw_onsets.Timestamps(i)
        output = ""
        for method_name in self.onset_method_names:
            timestamp = onsets.get(method_name, None)
            if timestamp is not None:
                if timestamp > 0:
                    output += f"{method_name}: X "
                else:
                    output += f"{method_name}: _ "
        output.strip()
        print(output)
