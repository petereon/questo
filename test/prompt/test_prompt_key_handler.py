import pytest
from questo import prompt
from yakh.key import Keys, Key


@pytest.fixture
def prompt_state():
    return prompt.PromptState(
        value='test',
        cursor_position=0,
        completion=prompt.CompletionState(options=['test1', 'test2'], index=None, in_completion_ctx=False),
    )


def test_tab_key_starts_completion(prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Key('\t', Keys.TAB, True))
    assert prompt_state.completion.in_completion_ctx is True
    assert prompt_state.completion.index == 0


def test_tab_increments_completion_index_when_in_completion_context(prompt_state):
    prompt_state.completion.in_completion_ctx = True
    prompt_state.completion.index = 0

    prompt_state = prompt.key_handler(prompt_state, Key('\t', Keys.TAB, True))
    assert prompt_state.completion.in_completion_ctx is True
    assert prompt_state.completion.index == 1


def test_tab_wraps_completion_index_when_in_completion_context(prompt_state):
    prompt_state.completion.in_completion_ctx = True
    prompt_state.completion.index = 1

    prompt_state = prompt.key_handler(prompt_state, Key('\t', Keys.TAB, True))
    assert prompt_state.completion.in_completion_ctx is True
    assert prompt_state.completion.index == 0


def test_ctrl_c_sets_abort_flag_and_clears_value(prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.CTRL_C)
    assert prompt_state.abort is True
    assert prompt_state.value is None


def test_enter_sets_exit_flag(prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.ENTER)
    assert prompt_state.exit is True


def test_left_arrow_decrements_cursor_position(prompt_state):
    prompt_state.cursor_position = 1
    prompt_state = prompt.key_handler(prompt_state, Keys.LEFT_ARROW)
    assert prompt_state.cursor_position == 0


def test_left_arrow_stops_decrementing_cursor_position_at_0(prompt_state):
    prompt_state.cursor_position = 0
    prompt_state = prompt.key_handler(prompt_state, Keys.LEFT_ARROW)
    assert prompt_state.cursor_position == 0


def test_right_arrow_increments_cursor_position(prompt_state):
    prompt_state.cursor_position = 0
    prompt_state = prompt.key_handler(prompt_state, Keys.RIGHT_ARROW)
    assert prompt_state.cursor_position == 1


def test_right_arrow_stops_incrementing_cursor_position_at_value_length(prompt_state):
    prompt_state.cursor_position = 1
    prompt_state.value = 'a'
    prompt_state = prompt.key_handler(prompt_state, Keys.RIGHT_ARROW)
    assert prompt_state.cursor_position == 1


def test_home_button_moves_cursor_to_0(prompt_state):
    prompt_state.cursor_position = 3
    prompt_state = prompt.key_handler(prompt_state, Keys.HOME)
    assert prompt_state.cursor_position == 0


def test_end_button_moves_cursor_to_value_length(prompt_state):
    prompt_state.cursor_position = 0
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.END)
    assert prompt_state.cursor_position == 4


def test_delete_removes_character_at_cursor_position(prompt_state):
    prompt_state.cursor_position = 1
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.DELETE)
    assert prompt_state.value == 'tst'
    assert prompt_state.cursor_position == 1


def test_delete_does_nothing_at_end_of_value(prompt_state):
    prompt_state.cursor_position = 4
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.DELETE)
    assert prompt_state.value == 'test'
    assert prompt_state.cursor_position == 4


def test_backspace_removes_character_before_cursor_position(prompt_state):
    prompt_state.cursor_position = 1
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.BACKSPACE)
    assert prompt_state.value == 'est'
    assert prompt_state.cursor_position == 0


def test_backspace_does_nothing_at_start_of_value(prompt_state):
    prompt_state.cursor_position = 0
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.BACKSPACE)
    assert prompt_state.value == 'test'
    assert prompt_state.cursor_position == 0


def test_escape_sets_exit_flag_and_clears_value(prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.ESC)
    assert prompt_state.exit is True
    assert prompt_state.value is None


def test_any_other_key_adds_character_at_cursor_position(prompt_state):
    prompt_state.value = 'bc'
    prompt_state.cursor_position = 0
    prompt_state = prompt.key_handler(prompt_state, Key('a', tuple(), True))
    assert prompt_state.value == 'abc'
    assert prompt_state.cursor_position == 1
