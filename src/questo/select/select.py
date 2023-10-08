from typing import Callable, Optional, Union

from rich.console import Console
from rich.live import Live
from yakh import get_key

from questo.internals import _cursor_hidden
from questo.select.navigation_handlers import DefaultNavigationHandler, INavigationHandler
from questo.select.renderers import DefaultRenderer, IRenderer
from questo.select.state import SelectState


class Select:
    """A select element."""

    navigation_handler: INavigationHandler
    renderer: IRenderer
    validator: Callable[[SelectState], SelectState]
    console: Console

    def __init__(
        self,
        navigation_handler: INavigationHandler = DefaultNavigationHandler(),
        renderer: IRenderer = DefaultRenderer(),
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

    def run(self, select_state: SelectState) -> Union[int, None]:
        with _cursor_hidden(self.console), Live("", console=self.console, auto_refresh=False, transient=True) as live:
            while True:
                select_state = self.step(select_state, live)
                if select_state.exit or select_state.abort:
                    break
        if select_state.select_multiple:
            return select_state.selected_indexes
        else:
            return select_state.index

    def step(self, select_state: SelectState, live_display: Live) -> SelectState:
        rendered = self.renderer.render(select_state)
        live_display.update(renderable=rendered)
        live_display.refresh()
        keypress = get_key()
        select_state.update(self.navigation_handler.handle(keypress, select_state))
        select_state.update(self.validator(select_state))
        return select_state
