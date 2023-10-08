from typing import Callable, Optional, Union

from rich.console import Console
from rich.live import Live
from yakh import get_key

from questo.internals import _cursor_hidden
from questo.prompt.navigation_handlers import DefaultNavigationHandler, INavigationHandler
from questo.prompt.renderers import DefaultRenderer, IRenderer
from questo.prompt.state import PromptState


class Prompt:
    """A prompt element."""

    navigation_handler: INavigationHandler
    renderer: IRenderer
    validator: Callable[[PromptState], PromptState]
    completion_handler: Callable[[PromptState], PromptState]
    console: Console

    def __init__(
        self,
        navigation_handler: INavigationHandler = DefaultNavigationHandler(),
        renderer: IRenderer = DefaultRenderer(),
        validator: Callable[[PromptState], PromptState] = lambda state: state,
        completion_handler: Callable[[PromptState], PromptState] = lambda value: [],
        console: Optional[Console] = None,
    ) -> None:
        self.navigation_handler = navigation_handler
        self.renderer = renderer
        self.validator = validator
        self.completion_handler = completion_handler
        if console is None:
            self.console = Console()
        else:
            self.console = console

    def run(self, prompt_state: PromptState) -> Union[int, None]:
        with _cursor_hidden(self.console), Live("", console=self.console, auto_refresh=False, transient=True) as live:
            while True:
                prompt_state = self.step(prompt_state, live)
                if prompt_state.exit or prompt_state.abort:
                    break
        if prompt_state.select_multiple:
            return prompt_state.selected_indexes
        else:
            return prompt_state.index

    def step(self, prompt_state: PromptState, live_display: Live) -> PromptState:
        rendered = self.renderer.render(prompt_state)
        live_display.update(renderable=rendered)
        live_display.refresh()
        keypress = get_key()
        prompt_state.update(self.navigation_handler.handle(keypress, prompt_state))
        prompt_state.update(self.validator(prompt_state))
        return prompt_state
