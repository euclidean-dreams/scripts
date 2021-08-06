from time import sleep

import flatbuffers
import zmq

from ImpresarioSerialization import OnsetProcessorParameters, IdentifierWrapper, Identifier
from ImpresarioSerialization.OnsetMethod import OnsetMethod


class ConductorMessenger:
    def __init__(self, context, endpoint):
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(endpoint)
        sleep(1)

    def send_threshold(self, onset_threshold):
        identityBuilder = flatbuffers.Builder(0)
        IdentifierWrapper.IdentifierWrapperStart(identityBuilder)
        IdentifierWrapper.IdentifierWrapperAddIdentifier(identityBuilder,
                                                         Identifier.Identifier.onsetProcessorParameters)
        identityBuilder.Finish(IdentifierWrapper.IdentifierWrapperEnd(identityBuilder))

        builder = flatbuffers.Builder(0)
        OnsetProcessorParameters.OnsetProcessorParametersStart(builder)
        OnsetProcessorParameters.OnsetProcessorParametersAddMethod(builder, OnsetMethod.specflux)
        OnsetProcessorParameters.OnsetProcessorParametersAddThreshold(builder, onset_threshold)
        OnsetProcessorParameters.OnsetProcessorParametersAddPeakPickingWindowSize(builder, 2)
        OnsetProcessorParameters.OnsetProcessorParametersAddPeakPickingWindowTailMultiplier(builder, 2)
        builder.Finish(OnsetProcessorParameters.OnsetProcessorParametersEnd(builder))
        message = [identityBuilder.Output(), builder.Output()]
        self.socket.send_multipart(message)
