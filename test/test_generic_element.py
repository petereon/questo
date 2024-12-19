from unittest import mock
from questo import select
from questo.abstract.abstract_element import GenericElement
import pytest


def test_generic_element_can_be_instantiated_without_arguments():
    try:
        GenericElement()
    except Exception:
        pytest.fail('Cannot be instantiated without arguments')


def test_generic_element_can_be_instantiated_with_arguments():
    try:
        GenericElement(renderer=lambda x: str(x))
    except Exception:
        pytest.fail('Cannot be instantiated with arguments')


def test_generic_element_does_not_mutate_the_original_state():
    selector = GenericElement()
    state = select.SelectState(title='A', options=[])
    selector.state = state
    state.title = 'B'
    assert selector.state.title == 'A', 'State was mutated'


def test_generic_element_states_does_not_get_mutated_unless_explicitly_assigned():
    selector = GenericElement()
    selector.state = select.SelectState(title='A', options=[])
    state = selector.state
    state.title = 'B'
    assert selector.state.title == 'A', 'State was not read'


def test_generic_element_displayed_creates_new_console_if_none_is_assigned_or_passed_and_destroys_it_right_after():
    selector = GenericElement()
    selector.state = select.SelectState(title='test', options=['a', 'b', 'c'], index=2)
    with selector.displayed():
        assert selector._console is not None


def test_generic_element_displayed_creates_new_live_display_and_destroys_it_right_after():
    selector = GenericElement()
    selector.state = select.SelectState(title='test', options=['a', 'b', 'c'], index=2)
    with selector.displayed():
        assert selector._live is not None
    assert selector._live is None


def test_generic_element_state_assignment_executes_the_rendering_handler():
    mock_renderer = mock.MagicMock(return_value='test')
    mock_live = mock.MagicMock()
    selector = GenericElement(renderer=mock_renderer)
    selector._live = mock_live
    state = select.SelectState(title='A', options=[])
    with selector.displayed():
        selector.state = state
    mock_renderer.assert_called_once_with(selector._state)
    mock_live.update.assert_called_once_with(renderable='test')
    mock_live.refresh.assert_called_once()


def test_generic_element_uses_the_console_provided_in_the_init_argument():
    mock_console = mock.MagicMock()
    selector = GenericElement(console=mock_console)
    select.SelectState(title='A', options=[])
    assert selector._console == mock_console


def test_generic_element_displayed_uses_the_console_provided_in_the_argument():
    selector = GenericElement()
    state = select.SelectState(title='A', options=[])
    selector.state = state
    mock_console = mock.MagicMock()
    with selector.displayed(console=mock_console):
        pass
    assert selector._console == mock_console
