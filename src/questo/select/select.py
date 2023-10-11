import copy
from typing import Callable, Optional, Tuple, Union

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
    validator: Callable[[SelectState], Tuple[bool, Optional[str]]]
    console: Console
    state: Union[SelectState, None] = None

    def __init__(
        self,
        navigation_handler: INavigationHandler = DefaultNavigationHandler(),
        renderer: IRenderer = DefaultRenderer(),
        validator: Callable[[SelectState], Tuple[bool, Optional[str]]] = lambda state: state,
        console: Optional[Console] = None,
    ) -> None:
        self.navigation_handler = navigation_handler
        self.renderer = renderer
        self.validator = validator
        if console is None:
            self.console = Console()
        else:
            self.console = console

    def use(self, state: SelectState) -> None:
        self.state = copy.deepcopy(state)

    def run(self) -> Union[int, None]:
        with _cursor_hidden(self.console), Live("", console=self.console, auto_refresh=False, transient=True) as live:
            while True:
                self.state = self.step(live)
                if self.state.exit or self.state.abort:
                    break
        if self.state.select_multiple:
            return self.state.selected_indexes
        else:
            return self.state.index

    def step(self, live_display: Live) -> SelectState:
        if not self.state:
            raise RuntimeError("No state provided. Use Select.use() to provide a state.")
        rendered = self.renderer.render(self.state)
        live_display.update(renderable=rendered)
        live_display.refresh()
        keypress = get_key()
        self.state = self.navigation_handler.handle(keypress, self.state)
        valid, err_str = self.validator(self.state)
        if not valid:
            self.state.error = err_str
        return self.state
