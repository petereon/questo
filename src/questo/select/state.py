from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class SelectState:
    """
    State of a select element.

    Attributes:
        options (List[str]): List of options to choose from.
        title (Optional[str]): Title displayed above the list. Defaults to None.
        select_multiple (bool): Enable multiple selection. Defaults to False.
        selected_indexes (List[int]): List of currently selected indexes (for multi-select). Defaults to [].
        index (Union[int, None]): Currently highlighted index. Defaults to 0.
        filter (str): Current filter string. Defaults to ''.
        pagination (bool): Enable pagination. Defaults to False.
        page_size (int): Number of items per page. Defaults to 5.
        error (Optional[str]): Error message to display. Defaults to None.
        exit (bool): True if the selection loop should exit. Defaults to False.
        abort (bool): True if the selection was aborted. Defaults to False.
    """

    options: List[str]
    title: Optional[str] = None
    select_multiple: bool = False
    selected_indexes: List[int] = field(default_factory=list)
    index: Union[int, None] = 0
    filter: str = ''
    pagination: bool = False
    page_size: int = 5
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False
