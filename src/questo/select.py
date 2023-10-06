from dataclasses import dataclass
from typing import Callable, List, Optional, Union

from rich.console import Console, RenderableType
from rich.live import Live
from rich.style import Style, StyleType
from yakh import get_key
from yakh.key import Key, Keys

from questo.internals import _apply_style, _cursor_hidden

# TODO: Think about separating the renderers and naviation_handlers into separate files without creating a circular import

@dataclass
class SelectState:
    """State of a select question."""

    options: List[str]
    title: Optional[str] = None
    index: Union[int, None] = 0
    filter: str = ""
    pagination: bool = False
    page_size: int = 5
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False

    def update(self, new_state: "SelectState") -> None:
        self.options = new_state.options
        self.title = new_state.title
        self.index = new_state.index
        self.filter = new_state.filter
        self.pagination = new_state.pagination
        self.page_size = new_state.page_size
        self.exit = new_state.exit
        self.abort = new_state.abort
        self.error = new_state.error


def default_navigation_handler(keypress: Key, select_state: SelectState) -> SelectState:
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
        return min([i for i in filtered_indexes if i >= index - step]) or min(filtered_indexes)


def increment_index(index, filtered_indexes, step):
    if filtered_indexes:
        return max([i for i in filtered_indexes if i <= index + step]) or max(filtered_indexes)


def get_filtered_indexes(select_state, filter):
    filtered_options = [i for i, option in enumerate(select_state.options) if filter in option]
    return filtered_options


def default_renderer(
    state: SelectState,
    title_style: StyleType = "bold",
    cursor: str = ">",
    cursor_style: StyleType = "pink1",
) -> RenderableType:
    # TODO: Deal with pagiantion on the renderer
    if isinstance(title_style, str):
        title_style: Style = Style.parse(title_style)
    if isinstance(cursor_style, str):
        cursor_style: Style = Style.parse(cursor_style)
    filter = f"{_apply_style(state.filter, 'grey42')}" if state.filter else ""
    title = _apply_style(f"{state.title}" if state.title else "", title_style)
    error = _apply_style(f"\n{state.error}" if state.error else "", "red")
    cursor = _apply_style(cursor, cursor_style)
    repr = [
        f"{title} {filter}\n",
        "\n".join(f'{cursor if state.index == i else " "} {option}' for i, option in enumerate(state.options) if state.filter in option),
        error,
    ]
    return "".join(repr)


class Select:
    """A select question."""

    navigation_handler: Callable[[Key], SelectState]
    renderer: Callable[[SelectState], RenderableType]
    validator: Callable[[SelectState], SelectState]
    console: Console

    def __init__(
        self,
        navigation_handler: Callable[[Key, SelectState], SelectState] = default_navigation_handler,
        renderer: Callable[[SelectState], RenderableType] = default_renderer,
        validator: Callable[[SelectState], SelectState] = lambda state: state,
        console: Optional[Console] = None,
    ) -> None:
        self.navigation_handler = navigation_handler
        self.renderer = renderer
        self.validator = validator
        if console is None:
            self.console = Console()
        else:
            self.console = console

    def run(self, select_state: SelectState) -> int:
        with _cursor_hidden(self.console), Live("", console=self.console, auto_refresh=False, transient=True) as live:
            while True:
                rendered = self.renderer(select_state)
                live.update(renderable=rendered)
                live.refresh()
                keypress = get_key()
                select_state.update(self.navigation_handler(keypress, select_state))
                select_state.update(self.validator(select_state))
                if select_state.exit or select_state.abort:
                    break
        return select_state.index
