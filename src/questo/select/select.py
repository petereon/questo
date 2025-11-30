from typing import Callable, Optional, Union

from rich.console import Console

from questo.abstract.abstract_element import GenericElement
from questo.internals import _NO_STATE_ERROR
from questo.select.renderer import DefaultRenderer
from questo.select.state import SelectState


class Select(GenericElement[SelectState]):
    """
    A select element for choosing options from a list.

    This element allows the user to select one or multiple options from a list, with support for filtering and pagination.
    """

    def __init__(
        self,
        state: Union[SelectState, None] = None,
        renderer: Callable[[SelectState], str] = DefaultRenderer().render,
        console: Optional[Console] = Console(highlight=False),
        transient: bool = True,
    ) -> None:
        """
        Initializes the Select element.

        Args:
            state (Union[SelectState, None], optional): Initial state of the select element. Defaults to None.
            renderer (Callable[[SelectState], str], optional): Function to render the state. Defaults to DefaultRenderer().render.
            console (Optional[Console], optional): Rich console instance. Defaults to Console(highlight=False).
            transient (bool, optional): Whether the element should disappear after completion. Defaults to True.
        """
        super().__init__(state=state, renderer=renderer, console=console, transient=transient)

    @property
    def result(self) -> Union[int, None]:
        """
        Returns the index of the selected option.

        Returns:
            Union[int, None]: The index of the selected option, or None if no option is selected.

        Raises:
            RuntimeError: If the state is None.
        """
        if self._state is None:
            raise _NO_STATE_ERROR
        return self._state.index
