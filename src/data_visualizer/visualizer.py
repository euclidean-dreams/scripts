import numpy as np
import zmq
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, LogColorMapper, LinearColorMapper
from bokeh.palettes import Inferno256
from bokeh.plotting import figure

from signaler import Signaler
from stft_receiver import STFTReceiver

TITLE = "Spectrogram"
MAX_STFT_COUNT = 50
STFT_SIZE = 257
X_AXIS_LABEL = "x"
Y_AXIS_LABEL = "y"
CONDUCTOR_DATA_ENDPOINT = "tcp://10.0.0.181:44442"

document = curdoc()
spectrogram = np.zeros((MAX_STFT_COUNT, STFT_SIZE))

data = {
    "image": [spectrogram.T]
}
source = ColumnDataSource(data=data)

output = figure(title=TITLE, x_axis_label=X_AXIS_LABEL, y_axis_label=Y_AXIS_LABEL, sizing_mode="stretch_both")
output.x_range.range_padding = 0
output.y_range.range_padding = 0

color_mapper = LinearColorMapper(palette=Inferno256, high=1)

output.image(source=source, x=0, y=0, dw=10, dh=10, color_mapper=color_mapper)

signaler = Signaler()
context = zmq.Context()
stft_receiver = STFTReceiver(document, source, spectrogram, signaler, context, CONDUCTOR_DATA_ENDPOINT)

document.add_root(output)

stft_receiver.start()
