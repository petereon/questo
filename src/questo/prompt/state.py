from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CompletionState:
    options: List[str] = field(default_factory=list)
    index: Optional[int] = None
    in_completion_ctx: bool = False


@dataclass
class PromptState:
    """
    State of a prompt element.

    Attributes:
        value (str): Current input value. Defaults to ''.
        title (Optional[str]): Title displayed above the prompt. Defaults to None.
        cursor_position (int): Current cursor position. Defaults to 0.
        completion (CompletionState): State for autocompletion. Defaults to CompletionState().
        error (Optional[str]): Error message to display. Defaults to None.
        exit (bool): True if the prompt loop should exit (e.g. Enter pressed). Defaults to False.
        abort (bool): True if the prompt was aborted (e.g. Ctrl+C). Defaults to False.
    """

    value: str = ''
    title: Optional[str] = None
    cursor_position: int = 0
    completion: CompletionState = field(default_factory=CompletionState)
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False
