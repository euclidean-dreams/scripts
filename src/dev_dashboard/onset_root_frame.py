import PySimpleGUI as gui

from dev_dashboard.config import DEFAULT_ONSET_THRESHOLD, SIZE_MULTIPLIER, DEFAULT_ONSET_PEAK_PICKING_WINDOW_SIZE, \
    DEFAULT_ONSET_PEAK_PICKING_WINDOW_TAIL
from dev_dashboard.utils import get_onset_method_names


def create_onset_root_frame():
    onset_frames = []
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        onset_frame_layout = [
            [
                create_onset_threshold_slider(onset_method),
                create_onset_peak_picking_window_size_slider(onset_method),
                create_onset_peak_picking_window_tail_slider(onset_method)
            ]
        ]

        onset_frame = gui.Frame(
            f"{onset_method}",
            onset_frame_layout,
            key=f"onset_frame|{onset_method}",
            title_location=gui.TITLE_LOCATION_TOP,
            font=("Helvetica", round(15 * SIZE_MULTIPLIER)),
            relief=gui.RELIEF_RAISED,
            border_width=round(5 * SIZE_MULTIPLIER)

        )

        onset_frames.append(onset_frame)

    onset_root_frame = gui.Frame(
        "Onset Parameters",
        [onset_frames],
        key=f"onset_root_frame",
        title_location=gui.TITLE_LOCATION_TOP,
        font=("Helvetica", round(25 * SIZE_MULTIPLIER)),
        relief=gui.RELIEF_RAISED,
        border_width=round(10 * SIZE_MULTIPLIER)
    )

    return onset_root_frame


def create_onset_threshold_slider(onset_method):
    return gui.Slider(
        range=(0.0, 20),
        default_value=DEFAULT_ONSET_THRESHOLD,
        resolution=0.1,
        border_width=round(5 * SIZE_MULTIPLIER),
        key=f"onset_threshold|{onset_method}",
        size=(round(15 * SIZE_MULTIPLIER), round(40 * SIZE_MULTIPLIER))
    )


def create_onset_peak_picking_window_size_slider(onset_method):
    return gui.Slider(
        range=(1, 25),
        default_value=DEFAULT_ONSET_PEAK_PICKING_WINDOW_SIZE,
        resolution=1,
        border_width=round(5 * SIZE_MULTIPLIER),
        key=f"onset_peak_picking_window_size|{onset_method}",
        size=(round(15 * SIZE_MULTIPLIER), round(40 * SIZE_MULTIPLIER))
    )


def create_onset_peak_picking_window_tail_slider(onset_method):
    return gui.Slider(
        range=(1, 25),
        default_value=DEFAULT_ONSET_PEAK_PICKING_WINDOW_TAIL,
        resolution=1,
        border_width=round(5 * SIZE_MULTIPLIER),
        key=f"onset_peak_picking_window_tail|{onset_method}",
        size=(round(15 * SIZE_MULTIPLIER), round(40 * SIZE_MULTIPLIER))
    )


def bind_onset_threshold_sliders(window):
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        slider = window[f"onset_threshold|{onset_method}"]
        slider.bind("<ButtonRelease-1>", "|left_click_released")


def bind_onset_peak_picking_window_size_sliders(window):
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        slider = window[f"onset_peak_picking_window_size|{onset_method}"]
        slider.bind("<ButtonRelease-1>", "|left_click_released")


def bind_onset_peak_picking_window_tail_sliders(window):
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        slider = window[f"onset_peak_picking_window_tail|{onset_method}"]
        slider.bind("<ButtonRelease-1>", "|left_click_released")
