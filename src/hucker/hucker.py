from time import sleep, time_ns

import flatbuffers as flatbuffers
import zmq as zmq

from ImpresarioSerialization.Identifier import Identifier
from ImpresarioSerialization.IdentifierWrapper import IdentifierWrapperStart, IdentifierWrapperAddIdentifier, \
    IdentifierWrapperEnd
from ImpresarioSerialization.Luminary import LuminaryStartGlimpseVector, LuminaryStart, AddTimestamp, AddGlimpse, \
    LuminaryEnd

BIND = True
ENDPOINT = "tcp://0.0.0.0:44400"

VALUES = [1, 2, 3, 4]


class Hucker:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        if BIND:
            self.socket.bind(ENDPOINT)
        else:
            self.socket.connect(ENDPOINT)
        sleep(1)

    def send(self):
        identity_builder = flatbuffers.Builder(0)
        IdentifierWrapperStart(identity_builder)
        IdentifierWrapperAddIdentifier(
            identity_builder, Identifier.luminary
        )
        identity_builder.Finish(IdentifierWrapperEnd(identity_builder))

        payload_builder = flatbuffers.Builder(0)

        LuminaryStartGlimpseVector(payload_builder, len(VALUES))
        for item in reversed(VALUES):
            payload_builder.PrependInt8(item)
        value_offset = payload_builder.EndVector()

        LuminaryStart(payload_builder)
        timestamp = int(time_ns() / 1000)
        AddTimestamp(payload_builder, timestamp)
        AddGlimpse(payload_builder, value_offset)
        payload_builder.Finish(LuminaryEnd(payload_builder))
        message = [identity_builder.Output(), payload_builder.Output()]
        self.socket.send_multipart(message)


if __name__ == '__main__':
    hucker = Hucker()
    while True:
        input()
        hucker.send()
