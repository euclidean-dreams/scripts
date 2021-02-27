import PySimpleGUI as gui

from dev_dashboard.config import DEFAULT_ONSET_THRESHOLD, DEFAULT_ONSET_SILENCE
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
            font=("Helvetica", 15),
            relief=gui.RELIEF_RAISED,
            border_width=5

        )

        onset_frames.append(onset_frame)

    onset_root_frame = gui.Frame(
        "Onset Parameters",
        [onset_frames],
        key=f"onset_root_frame",
        title_location=gui.TITLE_LOCATION_TOP,
        font=("Helvetica", 25),
        relief=gui.RELIEF_RAISED,
        border_width=10
    )

    return onset_root_frame


def create_onset_threshold_slider(onset_method):
    return gui.Slider(
        range=(0.0, 2.5),
        default_value=DEFAULT_ONSET_THRESHOLD,
        resolution=0.01,
        border_width=5,
        key=f"onset_threshold|{onset_method}",
        size=(15, 40)
    )


def create_onset_silence_slider(onset_method):
    return gui.Slider(
        range=(-20, -90),
        default_value=DEFAULT_ONSET_SILENCE,
        resolution=1,
        border_width=5,
        key=f"onset_silence|{onset_method}",
        size=(15, 40)
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
