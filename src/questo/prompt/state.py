from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CompletionState:
    options: List[str] = field(default_factory=list)
    index: Optional[int] = None
    in_completion_ctx: bool = False


@dataclass
class PromptState:
    """State of a prompt element."""

    value: str = ''
    title: Optional[str] = None
    cursor_position: int = 0
    completion: CompletionState = field(default_factory=CompletionState)
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False
