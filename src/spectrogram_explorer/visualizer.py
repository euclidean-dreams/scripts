###
# Run this script to visualize collected stft data
###
import struct

import numpy
from bokeh.io import show
from bokeh.models import ColumnDataSource, LinearColorMapper
from bokeh.palettes import Inferno256
from bokeh.plotting import figure

TITLE = "Spectrogram"
X_AXIS_LABEL = "Time"
Y_AXIS_LABEL = "Bin"
INT_SIZE = 4
FLOAT_SIZE = 4


def visualize(input_file_name):
    raw_data = None
    with open(input_file_name, mode='rb') as input_file:
        raw_file_content = input_file.read()
        end_index = 0
        while end_index < len(raw_file_content):
            start_index = end_index
            end_index = end_index + INT_SIZE
            layer_count = struct.unpack("i", raw_file_content[start_index:end_index])[0]
            if raw_data is None:
                raw_data = [[] for i in range(layer_count)]
            start_index = end_index
            end_index = end_index + INT_SIZE
            buffer_size = struct.unpack("i", raw_file_content[start_index:end_index])[0]
            for layer in range(layer_count):
                start_index = end_index
                end_index = start_index + buffer_size * FLOAT_SIZE
                raw_data[layer].append(
                    list(struct.unpack("f" * buffer_size, raw_file_content[start_index:end_index]))
                )

    # want some data?
    # print(raw_data[0][821])

    layers = []
    for layer in raw_data:
        layers.append(numpy.array(layer).T)

    output = figure(
        title=TITLE, x_axis_label=X_AXIS_LABEL, y_axis_label=Y_AXIS_LABEL, sizing_mode="stretch_both",
        tools=["hover,wheel_zoom,box_zoom,pan,reset"],
        active_drag="pan",
        active_scroll="wheel_zoom",
        tooltips=[("value", "@image"), ("x", "$x"), ("y", "$y")]
    )
    output.x_range.range_padding = 0
    output.y_range.range_padding = 0

    for index, layer in enumerate(layers):
        source = ColumnDataSource(data={"image": [layer]})
        output.image(source=source, x=0, y=0, dw=layer.shape[1], dh=layer.shape[0],
                     color_mapper=LinearColorMapper(palette=Inferno256),
                     legend_label=f"Layer {index}")

        output.legend.location = "top_left"
        output.legend.click_policy = "hide"

    show(output)


if __name__ == '__main__':
    visualize("quickAndCurious.jl")
