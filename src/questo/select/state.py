from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class SelectState:
    """State of a select element."""

    options: List[str]
    title: Optional[str] = None
    select_multiple: bool = False
    selected_indexes: List[int] = field(default_factory=list)
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
        self.select_multiple = new_state.select_multiple
        self.selected_indexes = new_state.selected_indexes
        self.index = new_state.index
        self.filter = new_state.filter
        self.pagination = new_state.pagination
        self.page_size = new_state.page_size
        self.exit = new_state.exit
        self.abort = new_state.abort
        self.error = new_state.error
