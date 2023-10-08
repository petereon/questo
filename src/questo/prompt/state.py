from dataclasses import dataclass, field
from typing import List, Optional


class CompletionState:
    options: List[str] = field(default_factory=list)
    index: Optional[int] = None
    in_completion_ctx: bool = False


@dataclass
class PromptState:
    """State of a prompt element."""

    value: str = ""
    title: Optional[str] = None
    cursor_position: int = 0
    completion: CompletionState = CompletionState()
    error: Optional[str] = None
    exit: bool = False
    abort: bool = False

    def update(self, new_state: "PromptState") -> None:
        self.value = new_state.value
        self.title = new_state.title
        self.cursor_position = new_state.cursor_position
        self.completion = new_state.completion
        self.exit = new_state.exit
        self.abort = new_state.abort
        self.error = new_state.error
