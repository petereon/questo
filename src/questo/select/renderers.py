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
        tick: str = "✓",
        tick_style: StyleType = "green",
    ) -> None:
        self.title_style = title_style
        self.cursor = cursor
        self.cursor_style = cursor_style
        self.highlight_style = highlight_style
        self.tick = tick
        self.tick_style = tick_style

    def render(self, state: SelectState) -> RenderableType:
        # TODO: add support for pagination
        title_style: Style = parse_string_style(self.title_style)
        cursor_style: Style = parse_string_style(self.cursor_style)
        highlight_style: Style = parse_string_style(self.highlight_style)
        tick_style: Style = parse_string_style(self.tick_style)

        filter = _apply_style(f"{state.filter}", "pink1 underline") if state.filter else ""
        title = _apply_style(f"{state.title}" if state.title else "", title_style)
        error = _apply_style(f"\n{state.error}" if state.error else "", "red")
        cursor = _apply_style(self.cursor, cursor_style)
        tick = _apply_style(self.tick, tick_style)

        options = state.options

        rendered_options = []
        if state.select_multiple:
            for i, option in enumerate(options):
                rendered_options.append(f'{cursor if state.index == i else " "} {tick if i in state.selected_indexes else " "} {option}')

        else:
            for i, option in enumerate(options):
                matched = re.search(f"({state.filter})", option, re.IGNORECASE)
                if matched:
                    rendered_options.append(
                        f'{cursor if state.index == i else " "} {render_option(option, matched.group(0), highlight_style)}',
                    )

        repr = [
            f"{title} {filter}\n",
            "\n".join(rendered_options),
            error,
        ]
        rendered_options.clear()
        return "".join(repr)


def parse_string_style(style: StyleType) -> Style:
    return Style.parse(style) if isinstance(style, str) else style


def render_option(option: str, match: str, highlight_style: Style) -> str:
    if match:
        res = re.sub(match, _apply_style(match, highlight_style), option)
        return res
    else:
        return option
