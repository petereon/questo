import copy
import re

from yakh.key import Key, Keys

from questo.select.state import SelectState


def key_handler(select_state: SelectState, keypress: Key) -> SelectState:
    s = copy.deepcopy(select_state)
    filtered_indexes = get_filtered_indexes(s)

    if keypress == Keys.UP_ARROW and filtered_indexes:
        s.index = decrement_index(s.index, filtered_indexes, 1)
    elif keypress == Keys.DOWN_ARROW and filtered_indexes:
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
    elif keypress == ' ' and s.select_multiple:
        if s.index in s.selected_indexes:
            s.selected_indexes.remove(s.index)
        else:
            s.selected_indexes.append(s.index)
    elif keypress == Keys.ENTER:
        s.exit = True
        if not filtered_indexes:
            s.index = None
    elif keypress == Keys.ESC:
        s.index = None
        s.exit = True
    elif keypress == Keys.CTRL_C:
        s.index = None
        s.abort = True
    elif keypress == Keys.BACKSPACE and not s.select_multiple:
        s.filter = s.filter[:-1]
    elif keypress.is_printable and not s.select_multiple:
        s.filter = s.filter + keypress.key
        filtered_indexes = get_filtered_indexes(s)
        if s.index not in filtered_indexes and filtered_indexes:
            s.index = min(filtered_indexes)

    return s


def decrement_index(index, filtered_indexes, step):
    try:
        return max([i for i in filtered_indexes if i <= index - step])
    except ValueError:
        return max(filtered_indexes)


def increment_index(index, filtered_indexes, step):
    try:
        return min([i for i in filtered_indexes if i >= index + step])
    except ValueError:
        return min(filtered_indexes)


def get_filtered_indexes(select_state: SelectState):
    return [i for i, option in enumerate(select_state.options) if re.search(select_state.filter, option, re.IGNORECASE)]
