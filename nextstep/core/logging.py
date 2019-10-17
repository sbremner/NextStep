import json
from settings import LOG_FILE

# TODO: Maybe use a custom logger for write_event?
# import logging
# logger = logging.getLogger("NextStep")


def make_event(**kwargs):
    # Just return it as a dictionary for now
    return kwargs


def write_event(evt):
    # Just dump it to stdout for now
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(evt) + '\n')