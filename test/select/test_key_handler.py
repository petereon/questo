from ward import test, fixture
from questo import select

from yakh.key import Key, Keys

from questo.select.state import SelectState


@fixture
def select_state():
    return SelectState(
        title='test',
        options=['test1', 'test2', 'test3'],
        index=0,
        pagination=True,
        page_size=2,
        select_multiple=False,
    )


@test('Key handler with up arrow decrements index')
def _(select_state=select_state):
    select_state.index = 1
    assert select.key_handler(select_state, Keys.UP_ARROW).index == 0


@test('Key handler with up arrow wraps index to end of options if index is 0')
def _(select_state=select_state):
    select_state.index = 0
    assert select.key_handler(select_state, Keys.UP_ARROW).index == 2


@test('Key handler with down arrow increments index')
def _(select_state=select_state):
    assert select.key_handler(select_state, Keys.DOWN_ARROW).index == 1


@test('Key handler with down arrow wraps index to end of options if index is at the last option')
def _(select_state=select_state):
    select_state.index = 2
    assert select.key_handler(select_state, Keys.DOWN_ARROW).index == 0


@test('Key handler with right arrow increments index by page size if pagination is `True`')
def _(select_state=select_state):
    select_state.pagination = True
    assert select.key_handler(select_state, Keys.RIGHT_ARROW).index == 2


@test('Key handler with left arrow decrements index by page size if pagination is `True`')
def _(select_state=select_state):
    select_state.pagination = True
    select_state.index = 2
    assert select.key_handler(select_state, Keys.LEFT_ARROW).index == 0


@test('Key handler with left arrow does nothing if pagination is `False`')
def _(select_state=select_state):
    select_state.pagination = False
    select_state.index = 0
    assert select.key_handler(select_state, Key('', Keys.RIGHT_ARROW, False)).index == 0


@test('Key handler with left arrow does nothing if pagination is `False`')
def _(select_state=select_state):
    select_state.pagination = False
    select_state.index = 2
    assert select.key_handler(select_state, Key('', Keys.LEFT_ARROW, False)).index == 2


@test('Key handler with HOME key sets index to first option')
def _(select_state=select_state):
    select_state.index = 1
    assert select.key_handler(select_state, Keys.HOME).index == 0


@test('Key handler with END key sets index to first option')
def _(select_state=select_state):
    select_state.index = 1
    assert select.key_handler(select_state, Keys.END).index == 2


@test('Key handler with SPACE key does nothing if select multiple is `False`')
def _(select_state=select_state):
    select_state.select_multiple = False
    select_state.selected_indexes = [0]
    select_state.index = 0
    assert select.key_handler(select_state, Key(' ', (), True)).selected_indexes == [0]


@test('Key handler with SPACE key unchecks index if select multiple is `True`')
def _(select_state=select_state):
    select_state.select_multiple = True
    select_state.selected_indexes = [0]
    select_state.index = 0
    assert select.key_handler(select_state, ' ').selected_indexes == []


@test('Key handler with SPACE key checks index if select multiple is `True` and one index is set already')
def _(select_state=select_state):
    select_state.select_multiple = True
    select_state.selected_indexes = [0]
    select_state.index = 1
    assert select.key_handler(select_state, ' ').selected_indexes == [0, 1]


@test('Key handler with ENTER key sets exit flag')
def _(select_state=select_state):
    assert select.key_handler(select_state, Keys.ENTER).exit is True


@test('Key handler with ENTER key sets exit flag and set index to `None` if no options are available')
def _(select_state=select_state):
    select_state.filter = 'test4'
    assert select.key_handler(select_state, Keys.ENTER).exit is True


@test('Key handler with ESC key sets exit flag and sets index to `None`')
def _(select_state=select_state):
    state = select.key_handler(select_state, Keys.ESC)
    assert state.exit is True
    assert state.index is None


@test('Key handler with CTRL-C key sets exit flag and sets index to `None`')
def _(select_state=select_state):
    state = select.key_handler(select_state, Keys.CTRL_C)
    assert state.abort is True
    assert state.index is None


@test('Key handler with BACKSPACE key removes last character from filter')
def _(select_state=select_state):
    select_state.filter = 'test'
    select_state.select_multiple = False
    assert select.key_handler(select_state, Keys.BACKSPACE).filter == 'tes'


@test('Key handler with printable key adds key to filter')
def _(select_state=select_state):
    select_state.filter = 'tes'
    select_state.select_multiple = False
    assert select.key_handler(select_state, Key('t', (), True)).filter == 'test'


@test('Key handler with ENTER key sets exit flag and set index to `None` if no options are available')
def _(select_state=select_state):
    select_state.filter = 'test'
    select_state.index = 0
    assert select.key_handler(select_state, Key('2', (), True)).index == 1
