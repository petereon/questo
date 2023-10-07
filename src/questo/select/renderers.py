import re
from abc import ABC, abstractmethod

from rich.console import RenderableType
from rich.style import Style, StyleType

from questo.internals import _apply_style
from questo.select.state import SelectState


class IRenderer(ABC):
    @abstractmethod
    def render(self, state: SelectState) -> RenderableType:
        ...


class DefaultRenderer(IRenderer):
    def __init__(
        self,
        title_style: StyleType = "bold",
        cursor: str = ">",
        cursor_style: StyleType = "cyan1 bold",
        highlight_style: StyleType = "pink1 bold",
    ) -> None:
        self.title_style = title_style
        self.cursor = cursor
        self.cursor_style = cursor_style
        self.highlight_style = highlight_style

    def render(self, state: SelectState) -> RenderableType:
        title_style: Style = Style.parse(self.title_style) if isinstance(self.title_style, str) else self.title_style
        cursor_style: Style = Style.parse(self.cursor_style) if isinstance(self.cursor_style, str) else self.cursor_style
        highlight_style: Style = Style.parse(self.highlight_style) if isinstance(self.highlight_style, str) else self.highlight_style

        filter = f"{_apply_style(state.filter, 'grey42')}" if state.filter else ""
        title = _apply_style(f"{state.title}" if state.title else "", title_style)
        error = _apply_style(f"\n{state.error}" if state.error else "", "red")
        cursor = _apply_style(self.cursor, cursor_style)

        rendered_options = []
        for i, option in enumerate(state.options):
            matched = re.search(f"({state.filter})", option, re.IGNORECASE)
            if matched:
                rendered_options.append(f'{cursor if state.index == i else " "} {render_option(option, matched.group(0), highlight_style)}')

        repr = [
            f"{title} {filter}\n",
            "\n".join(rendered_options),
            error,
        ]
        rendered_options.clear()
        return "".join(repr)


def render_option(option: str, match: str, highlight_style: Style) -> str:
    if match:
        res = re.sub(match, _apply_style(match, highlight_style), option)
        return res
    else:
        return option
