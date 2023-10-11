import copy
from contextlib import contextmanager
from typing import Callable, Optional, Union

from rich.console import Console
from rich.live import Live

from questo.internals import _cursor_hidden
from questo.prompt.renderers import DefaultRenderer
from questo.prompt.state import PromptState

_NO_STATE_ERROR = RuntimeError("No state provided. Please assing a state to the Prompt.state property.")


class Prompt:
    """A prompt element."""

    rendering_handler: Callable[[PromptState], str]
    _state: Union[PromptState, None] = None
    _live: Union[Live, None] = None

    def __init__(
        self,
        render_handler: Callable[[PromptState], str] = DefaultRenderer().render,
        console: Optional[Console] = None,
    ) -> None:
        self.rendering_handler = render_handler
        if console is None:
            self.console = Console()
        else:
            self.console = console

    @contextmanager
    def diplayed(self, console: Optional[Console] = None) -> None:
        if self._state is None:
            raise _NO_STATE_ERROR
        if console is None:
            console = Console()
        with _cursor_hidden(self.console), Live("", console=console, auto_refresh=False, transient=True) as live:
            self._live = live
            self.state = self._state
            yield self

    @property
    def state(self) -> PromptState:
        return copy.deepcopy(self._state)

    @state.setter
    def state(self, state: PromptState) -> None:
        self._state = copy.deepcopy(state)
        if self._live is not None:
            rendered = self.rendering_handler(self._state)
            self._live.update(renderable=rendered)
            self._live.refresh()

    @property
    def result(self) -> str:
        if self._state is None:
            raise _NO_STATE_ERROR
        return copy.copy(self._state.value)
