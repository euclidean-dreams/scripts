###
# Run this script to visualize collected stft data
###
import math
import struct
import subprocess

import numpy
from bokeh.io import show
from bokeh.models import ColumnDataSource, LinearColorMapper
from bokeh.palettes import Inferno256
from bokeh.plotting import figure

TITLE = "Spectrogram"
X_AXIS_LABEL = "x"
Y_AXIS_LABEL = "y"
INT_SIZE = 4
FLOAT_SIZE = 4
DATA_KINDS = 5


def visualize(input_file_name):
    subprocess.run(["rsync", "-azP", f"conductor:/root/output/{input_file_name}", "."])

    raw_data = [[] for i in range(DATA_KINDS)]
    with open(input_file_name, mode='rb') as input_file:
        raw_file_content = input_file.read()
        end_index = 0
        while end_index < len(raw_file_content):
            start_index = end_index
            end_index = end_index + INT_SIZE
            buffer_size = struct.unpack("i", raw_file_content[start_index:end_index])[0]
            for data_class in range(DATA_KINDS):
                start_index = end_index
                end_index = start_index + buffer_size * FLOAT_SIZE
                raw_data[data_class].append(
                    list(struct.unpack("f" * buffer_size, raw_file_content[start_index:end_index]))
                )
    spectrogram = numpy.array(raw_data[0]).T

    # set all spectral flux 0's to nan for color mapping convenience
    for i in range(len(raw_data[1])):
        if raw_data[1][i] == 0:
            raw_data[1][i] = math.nan

    spectral_flux = numpy.array(raw_data[1]).T
    fluxy_flux = numpy.array(raw_data[2]).T
    peaks = numpy.array(raw_data[3]).T
    fired = numpy.array(raw_data[4]).T

    output = figure(
        title=TITLE, x_axis_label=X_AXIS_LABEL, y_axis_label=Y_AXIS_LABEL, sizing_mode="stretch_both",
        tools=["hover,box_zoom,pan,reset"],
        active_drag="box_zoom",
        tooltips=[("value", "@image"), ("x", "$x"), ("y", "$y")]
    )
    output.x_range.range_padding = 0
    output.y_range.range_padding = 0

    source = ColumnDataSource(data={"image": [spectrogram]})
    output.image(source=source, x=0, y=0, dw=spectrogram.shape[1], dh=spectrogram.shape[0], color_mapper=LinearColorMapper(palette=Inferno256),
                 legend_label="Spectrogram")

    source = ColumnDataSource(data={"image": [spectral_flux]})
    output.image(source=source, x=0, y=0, dw=spectral_flux.shape[1], dh=spectral_flux.shape[0], color_mapper=LinearColorMapper(palette=Inferno256),
                 legend_label="Spectral Flux")

    source = ColumnDataSource(data={"image": [fluxy_flux]})
    output.image(source=source, x=0, y=0, dw=fluxy_flux.shape[1], dh=fluxy_flux.shape[0], color_mapper=LinearColorMapper(palette=Inferno256),
                 legend_label="Fluxy Flux")

    source = ColumnDataSource(data={"image": [peaks]})
    output.image(source=source, x=0, y=0, dw=peaks.shape[1], dh=peaks.shape[0], color_mapper=LinearColorMapper(palette=Inferno256),
                 legend_label="Peaks")

    source = ColumnDataSource(data={"image": [fired]})
    output.image(source=source, x=0, y=0, dw=fired.shape[1], dh=fired.shape[0], color_mapper=LinearColorMapper(palette=Inferno256),
                 legend_label="Fired")

    output.legend.location = "top_left"
    output.legend.click_policy = "hide"

    show(output)


if __name__ == '__main__':
    # visualize("curious.jl")
    visualize("quickAndCurious.jl")
