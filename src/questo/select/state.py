from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class SelectState:
    """State of a select question."""

    options: List[str]
    title: Optional[str] = None
    index: Union[int, None] = 0
    filter: str = ""
    pagination: bool = False
    page_size: int = 5
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False

    def update(self, new_state: "SelectState") -> None:
        self.options = new_state.options
        self.title = new_state.title
        self.index = new_state.index
        self.filter = new_state.filter
        self.pagination = new_state.pagination
        self.page_size = new_state.page_size
        self.exit = new_state.exit
        self.abort = new_state.abort
        self.error = new_state.error
