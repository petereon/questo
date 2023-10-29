from rich.console import RenderableType
from rich.style import Style, StyleType

from questo.internals import _apply_style, _parse_string_style
from questo.prompt.state import PromptState


class DefaultRenderer:
    def __init__(
        self,
        title_style: StyleType = 'bold',
        prompt_char: str = '>',
        prompt_style: StyleType = 'cyan1 bold',
    ) -> None:
        self.title_style = title_style
        self.prompt_char = prompt_char
        self.prompt_style = prompt_style

    def render(
        self,
        state: PromptState,
    ) -> RenderableType:
        title_style: Style = _parse_string_style(self.title_style)
        prompt_style: Style = _parse_string_style(self.prompt_style)

        title = _apply_style(f'{state.title} ' if state.title else '', title_style)
        prompt = _apply_style(f'{self.prompt_char}', prompt_style)
        error = _apply_style(f'{state.error}' if state.error else '', 'red')

        value_chars = [*state.value, ' ']
        value_chars[state.cursor_position] = _apply_style(value_chars[state.cursor_position], 'black on white')
        value = ''.join(value_chars)

        repr = [
            f'{prompt} {value}\n',
        ]

        if state.title:
            repr = [
                f'{title}\n',
                *repr,
            ]

        if state.error:
            repr = [
                *repr,
                f'{error}\n',
            ]

        options = state.completion.options
        if options and state.completion.in_completion_ctx:
            options[state.completion.index] = _apply_style(options[state.completion.index], 'black on white')
            repr = [*repr, ' '.join(options)]

        return ''.join(repr)
