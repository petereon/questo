from typing import Callable, Optional

from rich.console import Console, RenderableType
from rich.live import Live
from yakh import get_key
from yakh.key import Key

from questo.internals import _cursor_hidden
from questo.select.navigation_handlers import default_navigation_handler
from questo.select.renderers import default_renderer
from questo.select.state import SelectState


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