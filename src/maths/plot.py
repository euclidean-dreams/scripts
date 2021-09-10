from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import LinearColorMapper, Slider
from bokeh.palettes import Viridis256, Cividis256
from bokeh.plotting import figure

from data_source_manager import DataSourceManger
from harmonic_transformer import HarmonicTransformer
from spectrogram_manager import SpectrogramManager

DATA_FILE_NAME = "../spectrogram_explorer/quickAndCurious.jl"
INITIAL_SPECTROGRAM_INDEX = 215
INITIAL_FREQUENCY = 30
INITIAL_PEAK_SQUISH = 1
MAX_PARTIALS = 5

spectrogram_manager = SpectrogramManager(DATA_FILE_NAME)
initial_signal = spectrogram_manager.get_signal(INITIAL_SPECTROGRAM_INDEX)
harmonic_transformer = HarmonicTransformer(initial_signal, INITIAL_FREQUENCY, INITIAL_PEAK_SQUISH, MAX_PARTIALS)
data_source_manager = DataSourceManger(initial_signal, harmonic_transformer)

document = curdoc()
viridis_color_mapper = LinearColorMapper(palette=Viridis256, high=1810)
cividis_color_mapper = LinearColorMapper(palette=Cividis256)

#
# frequency slider
#
frequency_slider = Slider(
    start=10,
    end=100,
    value=INITIAL_FREQUENCY,
    step=1 / MAX_PARTIALS,
    title="Frequency",
    sizing_mode="stretch_width"
)
peak_squish_slider = Slider(
    start=0,
    end=5,
    value=INITIAL_PEAK_SQUISH,
    step=0.1,
    title="Peak Squish",
    sizing_mode="stretch_width"
)
spectrogram_index_slider = Slider(
    start=0,
    end=spectrogram_manager.get_max_index(),
    value=INITIAL_SPECTROGRAM_INDEX,
    step=1,
    title="Spectrogram Index",
    sizing_mode="stretch_width"
)


def frequency_slider_callback(attr, old, new):
    harmonic_transformer.update_frequency(new)
    data_source_manager.update()


def peak_squish_slider_callback(attr, old, new):
    harmonic_transformer.update_peak_squish(new)
    data_source_manager.update()


def spectrogram_index_slider_callback(attr, old, new):
    signal = spectrogram_manager.get_signal(new)
    harmonic_transformer.update_signal(signal)
    data_source_manager.update_signal(signal)


frequency_slider.on_change('value', frequency_slider_callback)
peak_squish_slider.on_change('value', peak_squish_slider_callback)
spectrogram_index_slider.on_change('value', spectrogram_index_slider_callback)

#
# original signal plot
#
signal_plot = figure(
    title="Input Signal",
    x_axis_label="Frequency Bin",
    y_axis_label="Magnitude",
    plot_width=1650,
    plot_height=750,
    tools=["hover,wheel_zoom,pan,reset"],
    active_drag="pan",
    active_scroll="wheel_zoom",
    tooltips=[
        ("frequency bin", "@x"),
        ("magnitude", "@y")
    ]
)
signal_plot.line(
    source=data_source_manager.signal_data,
    line_alpha=1,
    line_color="#e68cd5"
)
signal_plot.dot(
    source=data_source_manager.signal_data,
    color={"field": "x", "transform": viridis_color_mapper},
    size=15
)

# #
# # harmonic transform output
# #
# harmonic_transform_output_plot = figure(
#     title="Harmonic Transform Output",
#     x_axis_label="Frequency Bin",
#     y_axis_label="Magnitude",
#     plot_width=1650,
#     plot_height=750,
#     tools=["hover,wheel_zoom,pan,reset"],
#     active_drag="pan",
#     active_scroll="wheel_zoom",
#     tooltips=[
#         ("frequency bin", "@x"),
#         ("magnitude", "@y")
#     ]
# )
# harmonic_transform_output_plot.line(
#     source=data_source_manager.harmonic_transform,
#     line_alpha=1,
#     line_color="#e68cd5"
# )
# harmonic_transform_output_plot.dot(
#     source=data_source_manager.harmonic_transform,
#     color={"field": "x", "transform": viridis_color_mapper},
#     size=15
# )

#
# harmonic transform intermediary plot
#
harmonic_transform_internal_plot = figure(
    title="Harmonic Transform Internals",
    x_axis_label="Original Frequency Bin",
    y_axis_label="Magnitude",
    plot_width=1650,
    plot_height=750,
    tools=["hover,wheel_zoom,pan,reset"],
    active_drag="pan",
    active_scroll="wheel_zoom",
    tooltips=[
        ("frequency bin", "@x"),
        ("magnitude", "@y")
    ]
)
harmonic_transform_internal_plot.line(
    source=data_source_manager.signal_data,
    line_color="#020061",
    legend_label="Original Signal"
)
harmonic_transform_internal_plot.line(
    source=data_source_manager.signal_derivative_data,
    line_color="#4f4cba",
    legend_label="Signal Derivative"
)
harmonic_transform_internal_plot.line(
    source=data_source_manager.harmonic_signal_data,
    line_color="#ffbe0d",
    legend_label="Comparison Signal"
)
harmonic_transform_internal_plot.line(
    source=data_source_manager.result_signal_data,
    line_color="#009c00",
    legend_label="Output Signal"
)
harmonic_transform_internal_plot.legend.location = "top_left"
harmonic_transform_internal_plot.legend.click_policy = "hide"

#
# harmonic transform integral plot
#
harmonic_transform_integral_plot = figure(
    title="Harmonic Transform Integral",
    x_axis_label="",
    y_axis_label="Integral Value",
    plot_width=150,
    plot_height=750,
    tools=["wheel_zoom,pan,reset"],
    active_drag="pan",
    active_scroll="wheel_zoom"
)
harmonic_transform_integral_plot.dot(
    source=data_source_manager.harmonic_integral_data,
    color="#fa2fce",
    size=100
)

layout = layout(
    [frequency_slider],
    [peak_squish_slider],
    [spectrogram_index_slider],
    [harmonic_transform_internal_plot, harmonic_transform_integral_plot],
    [signal_plot],
    # [harmonic_transform_output_plot]
)

document.add_root(layout)
