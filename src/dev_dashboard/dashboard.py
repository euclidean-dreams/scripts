import PySimpleGUI as gui
import zmq

from dev_dashboard.conductor_messenger import ConductorMessenger
from dev_dashboard.config import CONDUCTOR_PARAMETER_ENDPOINT, SIZE_MULTIPLIER
from dev_dashboard.onset_root_frame import create_onset_root_frame, bind_onset_threshold_sliders, \
    bind_onset_peak_picking_window_size_sliders, bind_onset_peak_picking_window_tail_sliders
from dev_dashboard.signaler import Signaler
from dev_dashboard.utils import get_onset_method_from_string, get_onset_method_names

signaler = Signaler()
context = zmq.Context()
messenger = ConductorMessenger(context, CONDUCTOR_PARAMETER_ENDPOINT)
messenger.initialize_onset_parameters_to_default()
# onset_receiver = OnsetReceiver(signaler, context, CONDUCTOR_OUTPUT_ENDPOINT)

gui.theme("Dark Purple 3")

output = gui.Output(
    size=(round(0), round(20 * SIZE_MULTIPLIER)),
    key="output",
    font=("Helvetica", round(25 * SIZE_MULTIPLIER))
)

layout = [
    [create_onset_root_frame()],
    # [output]
]

window = gui.Window(
    "Impresario Dashboard",
    layout=layout,
    location=(round(200 * SIZE_MULTIPLIER), round(200 * SIZE_MULTIPLIER)),
    finalize=True
)
bind_onset_threshold_sliders(window)
bind_onset_peak_picking_window_size_sliders(window)
bind_onset_peak_picking_window_tail_sliders(window)

# output.expand(expand_x=True)

# onset_receiver.start()

finished = False
while not finished:
    event, values = window.read()
    if event == gui.WINDOW_CLOSED:
        finished = True
    else:
        event_parts = event.split("|")
        if len(event_parts) == 3:
            element_category = event_parts[0]
            element_identifier = event_parts[1]
            event_type = event_parts[2]
            if element_category in \
                    ("onset_threshold", "onset_peak_picking_window_size", "onset_peak_picking_window_tail") \
                    and event_type == "left_click_released":
                if element_identifier == "master":
                    for onset_name in get_onset_method_names():
                        window[f"{element_category}|{onset_name}"].update(value=values[f"{element_category}|master"])
                        onset_method = get_onset_method_from_string(onset_name)
                        if element_category == "onset_threshold":
                            onset_threshold = values[f"onset_threshold|master"]
                            onset_peak_picking_window_size = values[f"onset_peak_picking_window_size|{onset_name}"]
                            onset_peak_picking_window_tail = values[f"onset_peak_picking_window_tail|{onset_name}"]
                        elif element_category == "onset_peak_picking_window_size":
                            onset_threshold = values[f"onset_threshold|{onset_name}"]
                            onset_peak_picking_window_size = values[f"onset_peak_picking_window_size|master"]
                            onset_peak_picking_window_tail = values[f"onset_peak_picking_window_tail|{onset_name}"]
                        elif element_category == "onset_peak_picking_window_tail":
                            onset_threshold = values[f"onset_threshold|{onset_name}"]
                            onset_peak_picking_window_size = values[f"onset_peak_picking_window_size|{onset_name}"]
                            onset_peak_picking_window_tail = values[f"onset_peak_picking_window_tail|master"]
                        else:
                            raise TypeError("got invalid element category")
                        messenger.send_onset_parameters(onset_method, onset_threshold, onset_peak_picking_window_size,
                                                        onset_peak_picking_window_tail)
                else:
                    onset_method = get_onset_method_from_string(element_identifier)
                    onset_threshold = values[f"onset_threshold|{element_identifier}"]
                    onset_peak_picking_window_size = values[f"onset_peak_picking_window_size|{element_identifier}"]
                    onset_peak_picking_window_tail = values[f"onset_peak_picking_window_tail|{element_identifier}"]
                    messenger.send_onset_parameters(onset_method, onset_threshold, onset_peak_picking_window_size,
                                                    onset_peak_picking_window_tail)

signaler.signal_shutdown()
window.close()
