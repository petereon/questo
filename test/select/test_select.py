import pytest
from questo import select
from questo.internals import _NO_STATE_ERROR


def test_generic_element_result_raises_error_if_no_state_assigned():
    selector = select.Select()
    with pytest.raises(RuntimeError) as e:
        _ = selector.result
    assert e.value == _NO_STATE_ERROR


def test_generic_element_result_returns_the_index_from_the_state():
    selector = select.Select()
    selector.state = select.SelectState(title='test', options=['a', 'b', 'c'], index=2)
    assert selector.result == 2
