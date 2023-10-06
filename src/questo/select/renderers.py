
from questo.internals import _apply_style
from questo.select.state import SelectState
from rich.console import RenderableType
from rich.style import Style, StyleType


def default_renderer(
    state: SelectState,
    title_style: StyleType = "bold",
    cursor: str = ">",
    cursor_style: StyleType = "pink1",
) -> RenderableType:
    # TODO: Deal with pagiantion on the renderer
    if isinstance(title_style, str):
        title_style: Style = Style.parse(title_style)
    if isinstance(cursor_style, str):
        cursor_style: Style = Style.parse(cursor_style)
    filter = f"{_apply_style(state.filter, 'grey42')}" if state.filter else ""
    title = _apply_style(f"{state.title}" if state.title else "", title_style)
    error = _apply_style(f"\n{state.error}" if state.error else "", "red")
    cursor = _apply_style(cursor, cursor_style)
    repr = [
        f"{title} {filter}\n",
        "\n".join(f'{cursor if state.index == i else " "} {option}' for i, option in enumerate(state.options) if state.filter in option),
        error,
    ]
    return "".join(repr)
