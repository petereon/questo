import re
from abc import ABC

from yakh.key import Key, Keys

from questo.select.state import SelectState


class INavigationHandler(ABC):
    def handle(self, keypress: Key, select_state: SelectState) -> SelectState:
        ...


class DefaultNavigationHandler(INavigationHandler):
    def handle(self, keypress: Key, select_state: SelectState) -> SelectState:
        index = select_state.index
        exit = select_state.exit
        abort = select_state.abort
        filter = select_state.filter
        filtered_indexes = get_filtered_indexes(select_state, filter)

        if keypress == Keys.UP_ARROW:
            index = decrement_index(index, filtered_indexes, 1)
        elif keypress == Keys.DOWN_ARROW:
            index = increment_index(index, filtered_indexes, 1)
        elif keypress == Keys.RIGHT_ARROW and select_state.pagination:
            index = increment_index(index, filtered_indexes, select_state.page_size)
        elif keypress == Keys.LEFT_ARROW and select_state.pagination:
            index = increment_index(index, filtered_indexes, select_state.page_size)
        elif keypress == Keys.HOME:
            if filtered_indexes:
                index = min(filtered_indexes)
        elif keypress == Keys.END:
            if filtered_indexes:
                index = max(filtered_indexes)
        elif keypress == Keys.ENTER:
            exit = True
            if not filtered_indexes:
                index = None
        elif keypress in [Keys.ESC, Keys.CTRL_C]:
            index = None
            abort = True
        elif keypress == Keys.BACKSPACE:
            filter = filter[:-1]
        elif keypress.is_printable:
            filter = filter + keypress.key
            filtered_indexes = get_filtered_indexes(select_state, filter)
            if index not in filtered_indexes and filtered_indexes:
                index = min(filtered_indexes)

        return SelectState(
            options=select_state.options,
            title=select_state.title,
            index=index,
            filter=filter,
            pagination=select_state.pagination,
            page_size=select_state.page_size,
            error=select_state.error,
            exit=exit,
            abort=abort,
        )


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


def get_filtered_indexes(select_state, filter):
    return [i for i, option in enumerate(select_state.options) if re.search(filter, option, re.IGNORECASE)]
