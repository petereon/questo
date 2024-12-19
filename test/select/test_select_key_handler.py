import pytest
from questo import select
from yakh.key import Key, Keys
from questo.select.state import SelectState

@pytest.fixture
def select_state():
    return SelectState(
        title='test',
        options=['test1', 'test2', 'test3'],
        index=0,
        pagination=True,
        page_size=2,
        select_multiple=False,
    )

def test_key_handler_with_up_arrow_decrements_index(select_state):
    select_state.index = 1
    assert select.key_handler(select_state, Keys.UP_ARROW).index == 0

def test_key_handler_with_up_arrow_wraps_index_to_end_of_options_if_index_is_0(select_state):
    select_state.index = 0
    assert select.key_handler(select_state, Keys.UP_ARROW).index == 2

def test_key_handler_with_down_arrow_increments_index(select_state):
    assert select.key_handler(select_state, Keys.DOWN_ARROW).index == 1

def test_key_handler_with_down_arrow_wraps_index_to_end_of_options_if_index_is_at_the_last_option(select_state):
    select_state.index = 2
    assert select.key_handler(select_state, Keys.DOWN_ARROW).index == 0

def test_key_handler_with_right_arrow_increments_index_by_page_size_if_pagination_is_true(select_state):
    select_state.pagination = True
    assert select.key_handler(select_state, Keys.RIGHT_ARROW).index == 2

def test_key_handler_with_left_arrow_decrements_index_by_page_size_if_pagination_is_true(select_state):
    select_state.pagination = True
    select_state.index = 2
    assert select.key_handler(select_state, Keys.LEFT_ARROW).index == 0

def test_key_handler_with_left_arrow_does_nothing_if_pagination_is_false(select_state):
    select_state.pagination = False
    select_state.index = 0
    assert select.key_handler(select_state, Key('', Keys.RIGHT_ARROW, False)).index == 0

def test_key_handler_with_left_arrow_does_nothing_if_pagination_is_false_2(select_state):
    select_state.pagination = False
    select_state.index = 2
    assert select.key_handler(select_state, Key('', Keys.LEFT_ARROW, False)).index == 2

def test_key_handler_with_home_key_sets_index_to_first_option(select_state):
    select_state.index = 1
    assert select.key_handler(select_state, Keys.HOME).index == 0

def test_key_handler_with_end_key_sets_index_to_last_option(select_state):
    select_state.index = 1
    assert select.key_handler(select_state, Keys.END).index == 2

def test_key_handler_with_space_key_does_nothing_if_select_multiple_is_false(select_state):
    select_state.select_multiple = False
    select_state.selected_indexes = [0]
    select_state.index = 0
    assert select.key_handler(select_state, Key(' ', (), True)).selected_indexes == [0]

def test_key_handler_with_space_key_unchecks_index_if_select_multiple_is_true(select_state):
    select_state.select_multiple = True
    select_state.selected_indexes = [0]
    select_state.index = 0
    assert select.key_handler(select_state, ' ').selected_indexes == []

def test_key_handler_with_space_key_checks_index_if_select_multiple_is_true_and_one_index_is_set_already(select_state):
    select_state.select_multiple = True
    select_state.selected_indexes = [0]
    select_state.index = 1
    assert select.key_handler(select_state, ' ').selected_indexes == [0, 1]

def test_key_handler_with_enter_key_sets_exit_flag(select_state):
    assert select.key_handler(select_state, Keys.ENTER).exit is True

def test_key_handler_with_enter_key_sets_exit_flag_and_set_index_to_none_if_no_options_are_available(select_state):
    select_state.filter = 'test4'
    assert select.key_handler(select_state, Keys.ENTER).exit is True

def test_key_handler_with_esc_key_sets_exit_flag_and_sets_index_to_none(select_state):
    state = select.key_handler(select_state, Keys.ESC)
    assert state.exit is True
    assert state.index is None

def test_key_handler_with_ctrl_c_key_sets_exit_flag_and_sets_index_to_none(select_state):
    state = select.key_handler(select_state, Keys.CTRL_C)
    assert state.abort is True
    assert state.index is None

def test_key_handler_with_backspace_key_removes_last_character_from_filter(select_state):
    select_state.filter = 'test'
    select_state.select_multiple = False
    assert select.key_handler(select_state, Keys.BACKSPACE).filter == 'tes'

def test_key_handler_with_printable_key_adds_key_to_filter(select_state):
    select_state.filter = 'tes'
    select_state.select_multiple = False
    assert select.key_handler(select_state, Key('t', (), True)).filter == 'test'

def test_key_handler_with_enter_key_sets_exit_flag_and_set_index_to_none_if_no_options_are_available_2(select_state):
    select_state.filter = 'test'
    select_state.index = 0
    assert select.key_handler(select_state, Key('2', (), True)).index == 1
