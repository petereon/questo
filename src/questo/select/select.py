import copy
from contextlib import contextmanager
from typing import Callable, Optional, Union

from rich.console import Console
from rich.live import Live

from questo.internals import _NO_STATE_ERROR, _cursor_hidden
from questo.select.renderers import DefaultRenderer
from questo.select.state import SelectState


class Select:
    """A select element."""

    rendering_handler: Callable[[SelectState], str]
    console: Console
    _state: Union[SelectState, None] = None
    _live: Union[Live, None] = None

    def __init__(
        self,
        rendering_handler: Callable[[SelectState], str] = DefaultRenderer().render,
        console: Optional[Console] = None,
    ) -> None:
        self.rendering_handler = rendering_handler
        if console is None:
            self.console = Console()
        else:
            self.console = console

    @contextmanager
    def diplayed(self, console: Optional[Console] = None) -> None:
        if self._state is None:
            raise _NO_STATE_ERROR
        if console is not None:
            self.console = console
        if self.console is None:
            self.console = Console()
        with _cursor_hidden(self.console), Live("", console=self.console, auto_refresh=False, transient=True) as live:
            self._live = live
            self.state = self._state
            yield

    @property
    def state(self) -> SelectState:
        return copy.deepcopy(self._state)

    @state.setter
    def state(self, state: SelectState) -> None:
        self._state = copy.deepcopy(state)
        if self._live is not None:
            rendered = self.rendering_handler(self._state)
            self._live.update(renderable=rendered)
            self._live.refresh()

    @property
    def result(self) -> str:
        if self._state is None:
            raise _NO_STATE_ERROR
        return copy.copy(self._state.index)
