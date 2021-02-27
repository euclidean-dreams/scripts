from time import sleep

import flatbuffers
import zmq

from ImpresarioSerialization import OnsetProcessorParameters
from dev_dashboard.config import DEFAULT_ONSET_THRESHOLD, DEFAULT_ONSET_SILENCE, ONSET_MINIOI
from dev_dashboard.utils import get_onset_method_names, get_onset_method_from_string


class ConductorMessenger:
    def __init__(self, context, endpoint):
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(endpoint)
        sleep(1)

    def initialize_onset_parameters_to_default(self):
        for onset_method_name in get_onset_method_names():
            onset_method = get_onset_method_from_string(onset_method_name)
            self.send_onset_parameters(onset_method, DEFAULT_ONSET_THRESHOLD, DEFAULT_ONSET_SILENCE)

    def send_onset_parameters(self, onset_method, onset_threshold, onset_silence):
        builder = flatbuffers.Builder(1024)
        OnsetProcessorParameters.OnsetProcessorParametersStart(builder)
        OnsetProcessorParameters.OnsetProcessorParametersAddMethod(builder, onset_method)
        OnsetProcessorParameters.OnsetProcessorParametersAddThreshold(builder, onset_threshold)
        OnsetProcessorParameters.OnsetProcessorParametersAddMinioiMs(builder, ONSET_MINIOI)
        OnsetProcessorParameters.OnsetProcessorParametersAddSilence(builder, onset_silence)
        OnsetProcessorParameters.OnsetProcessorParametersAddAdaptiveWhitening(builder, True)
        builder.Finish(OnsetProcessorParameters.OnsetProcessorParametersEnd(builder))
        message = [builder.Output()]
        self.socket.send_multipart(message)
