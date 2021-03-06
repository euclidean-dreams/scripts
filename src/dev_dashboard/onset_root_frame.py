import PySimpleGUI as gui

from dev_dashboard.config import DEFAULT_ONSET_THRESHOLD, DEFAULT_ONSET_SILENCE, SIZE_MULTIPLIER
from dev_dashboard.utils import get_onset_method_names


def create_onset_root_frame():
    onset_frames = []
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        onset_frame_layout = [
            [create_onset_threshold_slider(onset_method), create_onset_silence_slider(onset_method)]
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
        range=(0.0, 2.5),
        default_value=DEFAULT_ONSET_THRESHOLD,
        resolution=0.01,
        border_width=round(5 * SIZE_MULTIPLIER),
        key=f"onset_threshold|{onset_method}",
        size=(round(15 * SIZE_MULTIPLIER), round(40 * SIZE_MULTIPLIER))
    )


def create_onset_silence_slider(onset_method):
    return gui.Slider(
        range=(-20, -90),
        default_value=DEFAULT_ONSET_SILENCE,
        resolution=1,
        border_width=round(5 * SIZE_MULTIPLIER),
        key=f"onset_silence|{onset_method}",
        size=(round(15 * SIZE_MULTIPLIER), round(40 * SIZE_MULTIPLIER))
    )


def bind_onset_threshold_sliders(window):
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        slider = window[f"onset_threshold|{onset_method}"]
        slider.bind("<ButtonRelease-1>", "|left_click_released")


def bind_onset_silence_sliders(window):
    onset_methods = get_onset_method_names()
    onset_methods.append("master")
    for onset_method in onset_methods:
        slider = window[f"onset_silence|{onset_method}"]
        slider.bind("<ButtonRelease-1>", "|left_click_released")
