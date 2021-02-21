from time import sleep

import flatbuffers
import zmq

import OnsetProcessorParameters
from OnsetMethod import OnsetMethod

if __name__ == '__main__':
    onset_threshold = 0.7
    onset_silence = -50.0
    method = OnsetMethod.phase

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:44440")
    sleep(1)
    builder = flatbuffers.Builder(1024)
    OnsetProcessorParameters.OnsetProcessorParametersStart(builder)
    OnsetProcessorParameters.OnsetProcessorParametersAddMethod(builder, method)
    OnsetProcessorParameters.OnsetProcessorParametersAddThreshold(builder, onset_threshold)
    OnsetProcessorParameters.OnsetProcessorParametersAddMinioiMs(builder, 1)
    OnsetProcessorParameters.OnsetProcessorParametersAddSilence(builder, onset_silence)
    OnsetProcessorParameters.OnsetProcessorParametersAddAdaptiveWhitening(builder, True)
    builder.Finish(OnsetProcessorParameters.OnsetProcessorParametersEnd(builder))
    socket.send_multipart([builder.Output()])
