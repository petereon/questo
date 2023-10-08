import re
from abc import ABC, abstractmethod
from typing import List, Tuple

from rich.console import RenderableType
from rich.style import Style, StyleType

from questo.internals import _apply_style, parse_string_style
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
        title_style: Style = parse_string_style(self.title_style)
        cursor_style: Style = parse_string_style(self.cursor_style)
        highlight_style: Style = parse_string_style(self.highlight_style)
        tick_style: Style = parse_string_style(self.tick_style)

        filter_query = _apply_style(f"{state.filter}", "pink1 underline") if state.filter else ""
        title = _apply_style(f"{state.title} " if state.title else "", title_style)
        error = _apply_style(f"\n{state.error}" if state.error else "", "red")
        cursor = _apply_style(self.cursor, cursor_style)
        tick = _apply_style(self.tick, tick_style)

        options = list(
            filter(
                lambda o: o[1],
                [(i, re.search(f"({state.filter})", option, re.IGNORECASE), option) for i, option in enumerate(state.options)],
            ),
        )

        pagination_line = ""
        if state.pagination:
            options, current_page, total_pages = paginate(options, state.index, state.page_size)
            pagination_line = "".join(["•" if current_page == i else "◦" for i in range(total_pages)])

        if state.select_multiple:
            rendered_options = [
                f'{cursor if state.index == i else " "} {tick if i in state.selected_indexes else " "} {option}' for i, _, option in options
            ]
        else:
            rendered_options = [
                f'{cursor if state.index == i else " "} {render_option(option, matched.group(0), highlight_style)}'
                for i, matched, option in options
            ]

        repr = [
            f"{title}{filter_query}\n",
            "\n".join(rendered_options),
            f"\n{pagination_line}",
            error,
        ]
        rendered_options.clear()
        return "".join(repr)


def paginate(options: List[Tuple[int, re.Match, str]], index: int, page_size: int) -> Tuple[List[Tuple[int, re.Match, str]], int, int]:
    total_pages = max((len(options) + 1) // page_size, 1)
    current_page = min(index // page_size, total_pages)
    return options[current_page * page_size : min((current_page + 1) * page_size, len(options))], current_page, total_pages


def render_option(option: str, match: str, highlight_style: Style) -> str:
    if match:
        res = re.sub(match, _apply_style(match, highlight_style), option)
        return res
    else:
        return option
