import copy
import re
from abc import ABC

from yakh.key import Key, Keys

from questo.select.state import SelectState


class INavigationHandler(ABC):
    def handle(self, keypress: Key, select_state: SelectState) -> SelectState:
        ...


class DefaultNavigationHandler(INavigationHandler):
    def handle(self, keypress: Key, select_state: SelectState) -> SelectState:
        s = copy.deepcopy(select_state)
        filtered_indexes = get_filtered_indexes(s)

        if keypress == Keys.UP_ARROW:
            s.index = decrement_index(s.index, filtered_indexes, 1)
        elif keypress == Keys.DOWN_ARROW:
            s.index = increment_index(s.index, filtered_indexes, 1)
        elif keypress == Keys.RIGHT_ARROW and s.pagination:
            s.index = increment_index(s.index, filtered_indexes, s.page_size)
        elif keypress == Keys.LEFT_ARROW and s.pagination:
            s.index = decrement_index(s.index, filtered_indexes, s.page_size)
        elif keypress == Keys.HOME:
            if filtered_indexes:
                s.index = min(filtered_indexes)
        elif keypress == Keys.END:
            if filtered_indexes:
                s.index = max(filtered_indexes)
        elif keypress == " " and s.select_multiple:
            if s.index in s.selected_indexes:
                s.selected_indexes.remove(s.index)
            else:
                s.selected_indexes.append(s.index)
        elif keypress == Keys.ENTER:
            s.exit = True
            if not filtered_indexes:
                s.index = None
        elif keypress in [Keys.ESC, Keys.CTRL_C]:
            s.index = None
            s.abort = True
        elif keypress == Keys.BACKSPACE:
            s.filter = s.filter[:-1]
        elif keypress.is_printable and not s.select_multiple:
            s.filter = s.filter + keypress.key
            filtered_indexes = get_filtered_indexes(s)
            if s.index not in filtered_indexes and filtered_indexes:
                s.index = min(filtered_indexes)

        return s


def decrement_index(index, filtered_indexes, step):
    if filtered_indexes:
        try:
            return max([i for i in filtered_indexes if i <= index - step])
        except ValueError:
            return max(filtered_indexes)
    return None


def increment_index(index, filtered_indexes, step):
    if filtered_indexes:
        try:
            return min([i for i in filtered_indexes if i >= index + step])
        except ValueError:
            return min(filtered_indexes)
    return None


def get_filtered_indexes(select_state: SelectState):
    return [i for i, option in enumerate(select_state.options) if re.search(select_state.filter, option, re.IGNORECASE)]