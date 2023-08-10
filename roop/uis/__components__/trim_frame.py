from time import sleep
from typing import Any, Dict, Tuple, Optional

import gradio

import roop.globals
from roop.capturer import get_video_frame_total
from roop.uis import core as ui
from roop.uis.typing import Update
from roop.utilities import is_video

TRIM_FRAME_START_NUMBER: Optional[gradio.Number] = None
TRIM_FRAME_END_NUMBER: Optional[gradio.Number] = None


def render() -> None:
    global TRIM_FRAME_START_NUMBER
    global TRIM_FRAME_END_NUMBER

    with gradio.Box():
        trim_frame_start_number_args: Dict[str, Any] = {
            'label': 'TRIM FRAME START',
            'value': roop.globals.trim_frame_start,
            'visible': False
        }
        trim_frame_end_number_args: Dict[str, Any] = {
            'label': 'TRIM FRAME END',
            'value': roop.globals.trim_frame_end,
            'visible': False
        }
        if is_video(roop.globals.target_path):
            trim_frame_start_number_args['visible'] = True
            trim_frame_end_number_args['visible'] = True
        with gradio.Row():
            TRIM_FRAME_START_NUMBER = gradio.Number(**trim_frame_start_number_args)
            TRIM_FRAME_END_NUMBER = gradio.Number(**trim_frame_end_number_args)


def listen() -> None:
    target_file = ui.get_component('target_file')
    if target_file:
        target_file.change(remote_update, outputs=[TRIM_FRAME_START_NUMBER, TRIM_FRAME_END_NUMBER])
    TRIM_FRAME_START_NUMBER.change(lambda value: update_number('trim_frame_start', int(value)), inputs=TRIM_FRAME_START_NUMBER, outputs=TRIM_FRAME_START_NUMBER)
    TRIM_FRAME_END_NUMBER.change(lambda value: update_number('trim_frame_end', int(value)), inputs=TRIM_FRAME_END_NUMBER, outputs=TRIM_FRAME_END_NUMBER)


def remote_update() -> Tuple[Update, Update]:
    sleep(0.5)
    if is_video(roop.globals.target_path):
        video_frame_total = get_video_frame_total(roop.globals.target_path)
        roop.globals.trim_frame_start = 0
        roop.globals.trim_frame_end = video_frame_total
        return gradio.update(value=0, maximum=video_frame_total, visible=True), gradio.update(value=video_frame_total, maximum=video_frame_total, visible=True)
    return gradio.update(value=None, maximum=None, visible=False), gradio.update(value=None, maximum=None, visible=False)


def update_number(name: str, value: int) -> Update:
    setattr(roop.globals, name, value)
    return gradio.update(value=value)
