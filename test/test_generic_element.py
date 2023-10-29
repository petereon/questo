from unittest import mock
from questo import select
from questo.abstract.abstract_element import GenericElement
from ward import test


@test('GenericElement can be instantiated without arguments')
def _():
    try:
        GenericElement()
    except Exception:
        assert False, 'Cannot be instantiated without arguments'


@test('GenericElement can be instantiated with arguments')
def _():
    try:
        GenericElement(renderer=lambda x: str(x))
    except Exception:
        assert False, 'Cannot be instantiated with arguments'


@test("GenericElement doesn't mutate the original state")
def _():
    selector = GenericElement()
    state = select.SelectState(title='A', options=[])
    selector.state = state
    state.title = 'B'
    assert selector.state.title == 'A', 'State was mutated'


@test("GenericElement.states doesn't get mutated unless explicitly assigned")
def _():
    selector = GenericElement()
    selector.state = select.SelectState(title='A', options=[])
    state = selector.state
    state.title = 'B'
    assert selector.state.title == 'A', 'State was not read'


@test('GenericElement.displayed creates new console if none is assigned or passed and destroys it right after')
def _():
    selector = GenericElement()
    selector.state = select.SelectState(title='test', options=['a', 'b', 'c'], index=2)
    with selector.diplayed():
        assert selector._console is not None


@test('GenericElement.displayed creates new live display and destroys it right after')
def _():
    selector = GenericElement()
    selector.state = select.SelectState(title='test', options=['a', 'b', 'c'], index=2)
    with selector.diplayed():
        assert selector._live is not None
    assert selector._live is None


@test('GenericElement.state assignment executes the rendering handler')
def _():
    mock_renderer = mock.MagicMock(return_value='test')
    mock_live = mock.MagicMock()
    selector = GenericElement(renderer=mock_renderer)
    selector._live = mock_live
    state = select.SelectState(title='A', options=[])
    with selector.diplayed():
        selector.state = state
    mock_renderer.assert_called_once_with(selector._state)
    mock_live.update.assert_called_once_with(renderable='test')
    mock_live.refresh.assert_called_once()


@test('GenericElement uses the console provided in the init argument')
def _():
    mock_console = mock.MagicMock()
    selector = GenericElement(console=mock_console)
    select.SelectState(title='A', options=[])
    assert selector._console == mock_console


@test('GenericElement.displayed uses the console provided in the argument')
def _():
    selector = GenericElement()
    state = select.SelectState(title='A', options=[])
    selector.state = state
    mock_console = mock.MagicMock()
    with selector.diplayed(console=mock_console):
        pass
    assert selector._console == mock_console
