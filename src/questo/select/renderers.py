import re
from abc import ABC, abstractmethod
from typing import List, Tuple

from rich.console import RenderableType
from rich.style import Style, StyleType

from questo.internals import _apply_style, _parse_string_style
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
        title_style: Style = _parse_string_style(self.title_style)
        cursor_style: Style = _parse_string_style(self.cursor_style)
        highlight_style: Style = _parse_string_style(self.highlight_style)
        tick_style: Style = _parse_string_style(self.tick_style)

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
            options, current_page_index, total_pages = _paginate(options, state.index, state.page_size)
            pagination_line = "".join(["•" if current_page_index == i else "◦" for i in range(total_pages)])

        if state.select_multiple:
            rendered_options = [
                f'{cursor if state.index == i else " "} {tick if i in state.selected_indexes else " "} {option}' for i, _, option in options
            ]
        else:
            rendered_options = [
                f'{cursor if state.index == i else " "} {re.sub(matched.group(0), _apply_style(matched.group(0), highlight_style), option)}'
                for i, matched, option in options
            ]

        repr = [
            "\n".join(rendered_options),
            f"\n{pagination_line}",
            error,
        ]

        if state.title:
            repr = [f"{title}{filter_query}\n", *repr]
        else:
            repr = [*repr, f"{filter_query}\n"]

        if error:
            repr = [*repr, f"\n{error}"]

        rendered_options.clear()
        return "".join(repr)


def _paginate(options: List[Tuple[int, re.Match, str]], index: int, page_size: int) -> Tuple[List[Tuple[int, re.Match, str]], int, int]:
    total_pages = max((len(options) + 1) // page_size, 1)
    current_page_index = min(index // page_size, total_pages - 1)
    return (
        options[current_page_index * page_size : min((current_page_index + 1) * page_size, len(options))],
        current_page_index,
        total_pages,
    )
