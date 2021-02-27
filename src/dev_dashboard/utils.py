from inspect import getmembers

from ImpresarioSerialization.OnsetMethod import OnsetMethod


def get_onset_method_names():
    onset_method_count = 0
    for member in getmembers(OnsetMethod):
        if not member[0].startswith("__"):
            if onset_method_count < member[1]:
                onset_method_count = member[1]
    onset_method_count += 1

    onset_methods = [None] * onset_method_count
    for member in getmembers(OnsetMethod):
        if not member[0].startswith("__"):
            onset_methods[member[1]] = member[0]
    return onset_methods


def get_onset_method_from_string(method_name):
    for member in getmembers(OnsetMethod):
        if member[0] == method_name:
            return member[1]
    raise ValueError(f"invalid method name: {method_name}")


def get_onset_method_string_from_number(method_number):
    for member in getmembers(OnsetMethod):
        if member[1] == method_number:
            return member[0]
    raise ValueError(f"invalid method number: {method_number}")
