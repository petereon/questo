import copy
from contextlib import contextmanager
from typing import Callable, Generic, Optional, TypeVar, Union

from rich.console import Console
from rich.live import Live

from questo.internals import _cursor_hidden

S = TypeVar('S')


class GenericElement(Generic[S]):
    renderer: Union[Callable[[S], str], None]
    _console: Union[Console, None]
    _state: Union[S, None] = None
    _live: Union[Live, None] = None

    def __init__(
        self,
        state: Union[S, None] = None,
        renderer: Callable[[S], str] = lambda s: '',
        console: Optional[Console] = None,
    ) -> None:
        self.state = state
        self.renderer = renderer
        if console is None:
            self._console = Console()
        else:
            self._console = console

    @contextmanager
    def diplayed(self, console: Optional[Console] = None) -> None:
        if console is not None:
            self._console = console
        if self._state is not None:
            with _cursor_hidden(self._console), Live('', console=self._console, auto_refresh=False, transient=True) as live:
                self._live = live
                self.state = self._state
                yield
                self._live = None
        else:
            yield

    @property
    def state(self) -> S:
        return copy.deepcopy(self._state)

    @state.setter
    def state(self, state: S) -> None:
        self._state = copy.deepcopy(state)
        if self._live is not None:
            rendered = self.renderer(self._state)
            self._live.update(renderable=rendered)
            self._live.refresh()
