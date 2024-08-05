from typing import Callable, Optional, Union

from rich.console import Console

from questo.abstract.abstract_element import GenericElement
from questo.internals import _NO_STATE_ERROR
from questo.prompt.renderer import DefaultRenderer
from questo.prompt.state import PromptState


class Prompt(GenericElement[PromptState]):
    """A prompt element."""

    def __init__(
        self,
        state: Union[PromptState, None] = None,
        renderer: Callable[[PromptState], str] = DefaultRenderer().render,
        console: Optional[Console] = Console(highlight=False),
        transient: bool = True,
    ) -> None:
        super().__init__(state=state, renderer=renderer, console=console, transient=transient)

    @property
    def result(self) -> str:
        if self._state is None:
            raise _NO_STATE_ERROR
        return self._state.value
