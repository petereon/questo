from contextlib import contextmanager
from typing import Iterator

from rich.console import Console
from rich.style import StyleType


@contextmanager
def _cursor_hidden(console: Console) -> Iterator:
    console.show_cursor(False)
    yield
    console.show_cursor(True)


def _apply_style(text: str, style: StyleType) -> str:
    return f"[{style}]{text}[/{style}]"
