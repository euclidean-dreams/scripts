from time import sleep

import flatbuffers
import zmq

from ImpresarioSerialization import OnsetProcessorParameters, IdentifierWrapper, Identifier
from dev_dashboard.config import DEFAULT_ONSET_THRESHOLD, DEFAULT_ONSET_PEAK_PICKING_WINDOW_SIZE, \
    DEFAULT_ONSET_PEAK_PICKING_WINDOW_TAIL
from dev_dashboard.utils import get_onset_method_names, get_onset_method_from_string


class ConductorMessenger:
    def __init__(self, context, endpoint):
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(endpoint)
        sleep(1)

    def initialize_onset_parameters_to_default(self):
        for onset_method_name in get_onset_method_names():
            onset_method = get_onset_method_from_string(onset_method_name)
            self.send_onset_parameters(onset_method, DEFAULT_ONSET_THRESHOLD, DEFAULT_ONSET_PEAK_PICKING_WINDOW_SIZE,
                                       DEFAULT_ONSET_PEAK_PICKING_WINDOW_TAIL)

    def send_onset_parameters(self, onset_method, onset_threshold, peak_picking_window_size, peak_picking_window_tail):
        identityBuilder = flatbuffers.Builder(0)
        IdentifierWrapper.IdentifierWrapperStart(identityBuilder)
        IdentifierWrapper.IdentifierWrapperAddIdentifier(identityBuilder,
                                                         Identifier.Identifier.onsetProcessorParameters)
        identityBuilder.Finish(IdentifierWrapper.IdentifierWrapperEnd(identityBuilder))

        builder = flatbuffers.Builder(0)
        OnsetProcessorParameters.OnsetProcessorParametersStart(builder)
        OnsetProcessorParameters.OnsetProcessorParametersAddMethod(builder, onset_method)
        OnsetProcessorParameters.OnsetProcessorParametersAddThreshold(builder, onset_threshold)
        OnsetProcessorParameters.OnsetProcessorParametersAddPeakPickingWindowSize(builder,
                                                                                  round(peak_picking_window_size))
        OnsetProcessorParameters.OnsetProcessorParametersAddPeakPickingWindowTailMultiplier(builder,
                                                                                            round(
                                                                                                peak_picking_window_tail))
        builder.Finish(OnsetProcessorParameters.OnsetProcessorParametersEnd(builder))
        message = [identityBuilder.Output(), builder.Output()]
        self.socket.send_multipart(message)
