import pytest
from questo import prompt
from questo.internals import _NO_STATE_ERROR


def test_generic_element_result_raises_error_if_no_state_assigned():
    selector = prompt.Prompt()
    with pytest.raises(RuntimeError) as e:
        _ = selector.result
    assert e.value == _NO_STATE_ERROR


def test_generic_element_result_returns_the_index_from_the_state():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value')
    assert selector.result == 'Test value'
