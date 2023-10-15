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
    filter: str = ''
    pagination: bool = False
    page_size: int = 5
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False
