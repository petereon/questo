from contextlib import contextmanager
from typing import Iterator

from rich.console import Console
from rich.style import Style, StyleType

_NO_STATE_ERROR = RuntimeError('No state provided. Please assign a state to the `.state` property.')


@contextmanager
def _cursor_hidden(console: Console) -> Iterator:
    console.show_cursor(False)
    yield
    console.show_cursor(True)


def _apply_style(text: str, style: StyleType) -> str:
    return f'[{style}]{text}[/{style}]'


def _parse_string_style(style: StyleType) -> Style:
    return Style.parse(style) if isinstance(style, str) else style
