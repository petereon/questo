from ward import test, expect
from questo import select
from questo.internals import _NO_STATE_ERROR

@test("GenericElement.result raises an error if no state is assigned")
def _():
    selector = select.Select()
    with expect.raises(RuntimeError) as e:
        selector.result
        assert e.value == _NO_STATE_ERROR

@test("GenericElement.result returns the index from the state")
def _():
    selector = select.Select()
    selector.state = select.SelectState(title="test", options=['a', 'b', 'c'], index=2)
    assert selector.result == 2
