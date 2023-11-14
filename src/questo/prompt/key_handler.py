import copy
from typing import Tuple

from yakh.key import Key, Keys

from questo.prompt.state import PromptState


def key_handler(prompt_state: PromptState, keypress: Key) -> PromptState:
    s = copy.deepcopy(prompt_state)

    if keypress == Keys.TAB:
        if s.completion.in_completion_ctx and s.completion.options:
            s.completion.index, s.cursor_position, s.value = completions_options_step(s)
        else:
            s.completion.in_completion_ctx = True
            s.completion.index = 0
            s.value = s.completion.options[s.completion.index]
            s.cursor_position = len(s.value)
    else:
        s.completion.in_completion_ctx = False
        s.completion.options = []
        s.completion.index = None

    if keypress == Keys.CTRL_C:
        s.value = None
        s.abort = True
    elif keypress == Keys.ENTER:
        s.exit = True
    elif keypress == Keys.LEFT_ARROW:
        if s.cursor_position > 0:
            s.cursor_position -= 1
    elif keypress == Keys.RIGHT_ARROW:
        if s.cursor_position < len(s.value):
            s.cursor_position += 1
    elif keypress == Keys.HOME:
        s.cursor_position = 0
    elif keypress == Keys.END:
        s.cursor_position = len(s.value)
    elif keypress == Keys.DELETE:
        if s.cursor_position < len(s.value):
            value_chars = [*s.value]
            del value_chars[s.cursor_position]
            s.value = ''.join(value_chars)
    elif keypress == Keys.BACKSPACE:
        if s.cursor_position > 0:
            s.cursor_position -= 1
            value_chars = [*s.value]
            del value_chars[s.cursor_position]
            s.value = ''.join(value_chars)
    elif keypress == Keys.ESC:
        s.value = None
        s.exit = True
    elif keypress.is_printable:
        if not (keypress == Keys.TAB and s.completion.in_completion_ctx):
            value_chars = [*s.value]
            value_chars.insert(s.cursor_position, str(keypress))
            s.cursor_position += 1
            s.value = ''.join(value_chars)

    return s


def completions_options_step(state: PromptState) -> Tuple[int, int, str]:
    index = (state.completion.index + 1) % len(state.completion.options)
    value = state.completion.options[index]
    cursor_positon = len(value)
    return index, cursor_positon, value
