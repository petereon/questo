from ward import test, expect
from questo import prompt
from questo.internals import _NO_STATE_ERROR

@test("GenericElement.result raises an error if no state is assigned")
def _():
    selector = prompt.Prompt()
    with expect.raises(RuntimeError) as e:
        selector.result
        assert e.value == _NO_STATE_ERROR

@test("GenericElement.result returns the index from the state")
def _():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title="test", value="Test value")
    assert selector.result == "Test value"
