import copy
from abc import ABC

from yakh.key import Key, Keys

from questo.prompt.state import PromptState


class INavigationHandler(ABC):
    def handle(self, keypress: Key, select_state: PromptState) -> PromptState:
        ...


class DefaultNavigationHandler(INavigationHandler):
    def handle(self, keypress: Key, prompt_state: PromptState) -> PromptState:
        s = copy.deepcopy(prompt_state)

        if keypress == Keys.TAB:
            if s.completion.in_completion_ctx and s.completion.options:
                s.completion.index = (s.completion.index + 1) % len(s.completion.options)
                s.value = s.completion.options[s.completion.index]
            else:
                s.completion.in_completion_ctx = True
        else:
            s.completion.in_completion_ctx = False
            s.completion.options = []
            s.completion.index = None

        if keypress == Keys.CTRL_C:
            s.value = None
            s.completion.in_completion_ctx = False
        elif keypress == Keys.ENTER:
            s.exit = True
        elif keypress == Keys.BACKSPACE:
            if s.cursor_position > 0:
                s.cursor_position -= 1
                del s.value[s.cursor_position]
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
                del s.value[s.cursor_position]
        elif keypress == Keys.ESC:
            s.abort = True
        elif keypress:
            if not (keypress == Keys.TAB and s.completion.in_completion_ctx):
                s.value.insert(s.cursor_position, str(keypress))
                s.cursor_position += 1

        return s
