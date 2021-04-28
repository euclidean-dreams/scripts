import json

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import LinearColorMapper, Slider
from bokeh.palettes import Viridis256, Cividis256
from bokeh.plotting import figure

from auto_correlator import AutoCorrelator
from data_source_manager import DataSourceManger
from harmonic_transformer import HarmonicTransformer

DATA_FILE_NAME = "perpet-5_80.json"
INITIAL_FREQUENCY = 48
AUTO_CORRELATION_ITERATIONS = 2

with open(f"data/{DATA_FILE_NAME}", "r") as data_file:
    signal = json.load(data_file)

harmonic_transformer = HarmonicTransformer(signal, INITIAL_FREQUENCY)
auto_correlator = AutoCorrelator(signal, AUTO_CORRELATION_ITERATIONS, INITIAL_FREQUENCY)
data_source_manager = DataSourceManger(signal, harmonic_transformer, auto_correlator)

document = curdoc()
viridis_color_mapper = LinearColorMapper(palette=Viridis256, high=1810)
cividis_color_mapper = LinearColorMapper(palette=Cividis256)

#
# squash t plot
#
squash_t_plot = figure(
    title="Squash t",
    x_axis_label="Real",
    y_axis_label="Imaginary",
    plot_width=750,
    plot_height=750,
    tools=["crosshair,wheel_zoom,pan,reset"],
    active_drag="pan",
    active_scroll="wheel_zoom",
    tooltips=[
        ("t", "@t"),
        ("(real, imaginary)", "($x, $y)")
    ]
)

squash_t_plot.multi_line(
    source=data_source_manager.peak_vector_data,
    line_alpha=0.5,
    line_color={"field": "t", "transform": viridis_color_mapper}
)
squash_t_plot.dot(
    source=data_source_manager.harmonic_transform_data,
    color={"field": "t", "transform": viridis_color_mapper},
    size=15
)
squash_t_plot.line(source=data_source_manager.harmonic_transform_data, line_alpha=0.5, line_color="#e68cd5")

#
# frequency slider
#
frequency_slider = Slider(
    start=0,
    end=300,
    value=INITIAL_FREQUENCY,
    step=1,
    title="Frequency",
    sizing_mode="stretch_width"
)
iteration_slider = Slider(
    start=0,
    end=10,
    value=AUTO_CORRELATION_ITERATIONS,
    step=1,
    title="Autocorrelation iterations",
    sizing_mode="stretch_width"
)


def frequency_slider_callback(attr, old, new):
    # harmonic_transformer.calculate(new)
    auto_correlator.update_frequency(new)
    data_source_manager.update()


def iteration_slider_callback(attr, old, new):
    auto_correlator.update_iterations(new)
    data_source_manager.update()


frequency_slider.on_change('value', frequency_slider_callback)
iteration_slider.on_change('value', iteration_slider_callback)

#
# intersection with rt plane
#
intersection_plot = figure(
    title="Intersection With rt Plane",
    x_axis_label="t",
    y_axis_label="r",
    plot_width=750,
    plot_height=750,
    tools=["hover,wheel_zoom,pan,reset"],
    active_drag="pan",
    active_scroll="wheel_zoom"
)
intersection_plot.dot(
    source=data_source_manager.intersection_data,
    color={"field": "x", "transform": viridis_color_mapper},
    size=15
)
intersection_plot.line(
    source=data_source_manager.intersection_data,
    line_alpha=0.5,
    line_color="#e68cd5"
)
intersection_plot.dot(
    source=data_source_manager.intersection_integral_data,
    color="#ffbd08",
    size=50
)

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
signal_plot.dot(
    source=data_source_manager.signal_peak_data,
    color="#ffbd08",
    size=25
)

#
# harmonic transform plot
#
harmonic_transsform_plot = figure(
    title="Harmonic Transform",
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
harmonic_transsform_plot.multi_line(
    source=data_source_manager.shifted_signals,
    line_color={"field": "iteration", "transform": cividis_color_mapper}
)
harmonic_transsform_plot.line(
    source=data_source_manager.auto_correlated_signal,
    line_alpha=1,
    line_color="#20ff00"
)

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
    source=data_source_manager.auto_correlation_integral_data,
    color="#e278ff",
    size=100
)

layout = layout(
    # [squash_t_plot, intersection_plot],
    [frequency_slider],
    [iteration_slider],
    [harmonic_transsform_plot, harmonic_transform_integral_plot],
    [signal_plot]
)

document.add_root(layout)
