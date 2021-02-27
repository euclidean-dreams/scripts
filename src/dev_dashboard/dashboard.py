import PySimpleGUI as gui
import zmq

from dev_dashboard.audio_attributes_receiver import AudioAttributesReceiver
from dev_dashboard.conductor_messenger import ConductorMessenger
from dev_dashboard.config import CONDUCTOR_PARAMETER_ENDPOINT, CONDUCTOR_AUDIO_ATTRIBUTES_ENDPOINT
from dev_dashboard.onset_root_frame import create_onset_root_frame, bind_onset_threshold_sliders, \
    bind_onset_silence_sliders
from dev_dashboard.signaler import Signaler
from dev_dashboard.utils import get_onset_method_from_string, get_onset_method_names

signaler = Signaler()
context = zmq.Context()
messenger = ConductorMessenger(context, CONDUCTOR_PARAMETER_ENDPOINT)
messenger.initialize_onset_parameters_to_default()
attributes_receiver = AudioAttributesReceiver(signaler, context, CONDUCTOR_AUDIO_ATTRIBUTES_ENDPOINT)

gui.theme("Dark Purple 3")

output = gui.Output(
    size=(0, 10),
    key="output",
    font=("Helvetica", 15)
)

layout = [
    [create_onset_root_frame()],
    [output]
]

window = gui.Window(
    "Impresario Dashboard",
    layout=layout,
    location=(200, 200),
    finalize=True
)
bind_onset_threshold_sliders(window)
bind_onset_silence_sliders(window)

output.expand(expand_x=True)

attributes_receiver.start()

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
            if element_category in ("onset_threshold", "onset_silence") and event_type == "left_click_released":
                if element_identifier == "master":
                    for onset_name in get_onset_method_names():
                        window[f"{element_category}|{onset_name}"].update(value=values[f"{element_category}|master"])
                        onset_method = get_onset_method_from_string(onset_name)
                        if element_category == "onset_threshold":
                            onset_threshold = values[f"onset_threshold|master"]
                            onset_silence = values[f"onset_silence|{onset_name}"]
                        else:
                            onset_threshold = values[f"onset_threshold|{onset_name}"]
                            onset_silence = values[f"onset_silence|master"]
                        messenger.send_onset_parameters(onset_method, onset_threshold, onset_silence)
                else:
                    onset_method = get_onset_method_from_string(element_identifier)
                    onset_threshold = values[f"onset_threshold|{element_identifier}"]
                    onset_silence = values[f"onset_silence|{element_identifier}"]
                    messenger.send_onset_parameters(onset_method, onset_threshold, onset_silence)

signaler.signal_shutdown()
window.close()
