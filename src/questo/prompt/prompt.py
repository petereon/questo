from typing import Callable, Optional, Union

from rich.console import Console

from questo.abstract.abstract_element import GenericElement
from questo.internals import _NO_STATE_ERROR
from questo.prompt.renderer import DefaultRenderer
from questo.prompt.state import PromptState


class Prompt(GenericElement[PromptState]):
    """
    A prompt element for text input.

    This element allows the user to input text, with support for completions and cursor navigation.
    """

    def __init__(
        self,
        state: Union[PromptState, None] = None,
        renderer: Callable[[PromptState], str] = DefaultRenderer().render,
        console: Optional[Console] = Console(highlight=False),
        transient: bool = True,
    ) -> None:
        """
        Initializes the Prompt element.

        Args:
            state (Union[PromptState, None], optional): Initial state of the prompt. Defaults to None.
            renderer (Callable[[PromptState], str], optional): Function to render the state. Defaults to DefaultRenderer().render.
            console (Optional[Console], optional): Rich console instance. Defaults to Console(highlight=False).
            transient (bool, optional): Whether the element should disappear after completion. Defaults to True.
        """
        super().__init__(state=state, renderer=renderer, console=console, transient=transient)

    @property
    def result(self) -> str:
        """
        Returns the value from the state.

        Returns:
            str: The current input value.

        Raises:
            RuntimeError: If the state is None.
        """
        if self._state is None:
            raise _NO_STATE_ERROR
        return self._state.value
