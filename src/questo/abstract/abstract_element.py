import copy
from contextlib import contextmanager
from typing import Callable, Generator, Generic, Optional, TypeVar, Union

from rich.console import Console
from rich.live import Live

from questo.internals import _cursor_hidden

S = TypeVar('S')


class GenericElement(Generic[S]):
    renderer: Union[Callable[[S], str], None]
    transient: bool = True
    _console: Union[Console, None] = None
    _state: Union[S, None] = None
    _live: Union[Live, None] = None
    _reactive: bool = True
    _copy: bool = True

    def __init__(
        self,
        state: Union[S, None] = None,
        renderer: Callable[[S], str] = lambda s: '',
        console: Optional[Console] = Console(highlight=False),
        reactive: bool = True,
        copy: bool = True,
        transient: bool = True,
    ) -> None:
        """Creates a CLI Element

        Args:
            state (Union[S, None], optional): State of the CLI Element. Defaults to None.
            renderer (Callable[[S], str], optional): Callable that renders the state to string.
            console (Optional[Console], optional): rich.Console instance to use for displaying. Defaults to Console(highlight=False).
            reactive (bool, optional): Flag that configures whether the element automatically rerenders on state assignment.
            Defaults to True.
            copy (bool, optional): Flag that configures whether the state will be deep-copied when read or assigned. Defaults to True.
            transient (bool, optional): Flag that configures whether the rendering of the element will disappear after completing.
            Defaults to True.
        """
        self.state = state
        self.renderer = renderer
        self._reactive = reactive
        self._copy = copy
        self._console = console
        self.transient = transient

    @contextmanager
    def displayed(self, console: Optional[Console] = None) -> Generator[None, None, None]:
        """Context that displays the element

        Args:
            console (Optional[Console], optional): rich.Console instance to use for displaying. Defaults to None.
        """
        if console is not None:
            self._console = console
        if self._state is not None:
            with _cursor_hidden(self._console), Live('', console=self._console, auto_refresh=False, transient=self.transient) as live:
                self._live = live
                self.state = self._state
                yield
                self._live = None
        else:
            yield

    @property
    def state(self) -> S:
        if self._copy:
            return copy.deepcopy(self._state)
        return self._state

    @state.setter
    def state(self, state: S) -> None:
        if self._copy:
            self._state = copy.deepcopy(state)
        else:
            self._state = state
        if self._live is not None and self._reactive:
            self.update()

    def update(self) -> None:
        """Updates the displayed element"""
        rendered = self.renderer(self._state)
        self._live.update(renderable=rendered)
        self._live.refresh()
