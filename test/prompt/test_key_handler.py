from ward import test, fixture
from questo import prompt
from yakh.key import Keys


@fixture
def prompt_state():
    return prompt.PromptState(
        value='test',
        cursor_position=0,
        completion=prompt.CompletionState(options=['test1', 'test2'], index=None, in_completion_ctx=False),
    )


@test('Tab key starts completion')
def _(prompt_state=prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.TAB)
    assert prompt_state.completion.in_completion_ctx is True
    assert prompt_state.completion.index == 0


@test('Tab increments completion index when in completion context')
def _(prompt_state=prompt_state):
    prompt_state.completion.in_completion_ctx = True
    prompt_state.completion.index = 0

    prompt_state = prompt.key_handler(prompt_state, Keys.TAB)
    assert prompt_state.completion.in_completion_ctx is True
    assert prompt_state.completion.index == 1


@test('Tab wraps completion index when in completion context')
def _(prompt_state=prompt_state):
    prompt_state.completion.in_completion_ctx = True
    prompt_state.completion.index = 1

    prompt_state = prompt.key_handler(prompt_state, Keys.TAB)
    assert prompt_state.completion.in_completion_ctx is True
    assert prompt_state.completion.index == 0


@test('Ctrl-C sets abort flag and clears value')
def _(prompt_state=prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.CTRL_C)
    assert prompt_state.abort is True
    assert prompt_state.value is None


@test('Enter sets exit flag')
def _(prompt_state=prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.ENTER)
    assert prompt_state.exit is True


@test('Left arrow decrements cursor position')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 1
    prompt_state = prompt.key_handler(prompt_state, Keys.LEFT_ARROW)
    assert prompt_state.cursor_position == 0


@test('Left arrow stops decrementing cursor position at 0')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 0
    prompt_state = prompt.key_handler(prompt_state, Keys.LEFT_ARROW)
    assert prompt_state.cursor_position == 0


@test('Right arrow increments cursor position')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 0
    prompt_state = prompt.key_handler(prompt_state, Keys.RIGHT_ARROW)
    assert prompt_state.cursor_position == 1


@test('Right arrow stops incremeting cursor position at value length')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 1
    prompt_state.value = 'a'
    prompt_state = prompt.key_handler(prompt_state, Keys.RIGHT_ARROW)
    assert prompt_state.cursor_position == 1


@test('Home button moves cursor to 0')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 3
    prompt_state = prompt.key_handler(prompt_state, Keys.HOME)
    assert prompt_state.cursor_position == 0


@test('End button moves cursor to value length')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 0
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.END)
    assert prompt_state.cursor_position == 4


@test('Delete removes character at cursor position')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 1
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.DELETE)
    assert prompt_state.value == 'tst'
    assert prompt_state.cursor_position == 1


@test('Delete does nothing at end of value')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 4
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.DELETE)
    assert prompt_state.value == 'test'
    assert prompt_state.cursor_position == 4


@test('Backspace removes character before cursor position')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 1
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.BACKSPACE)
    assert prompt_state.value == 'est'
    assert prompt_state.cursor_position == 0


@test('Backspace does nothing at start of value')
def _(prompt_state=prompt_state):
    prompt_state.cursor_position = 0
    prompt_state.value = 'test'
    prompt_state = prompt.key_handler(prompt_state, Keys.BACKSPACE)
    assert prompt_state.value == 'test'
    assert prompt_state.cursor_position == 0


@test('Escape sets exit flag and clears value')
def _(prompt_state=prompt_state):
    prompt_state = prompt.key_handler(prompt_state, Keys.ESC)
    assert prompt_state.exit is True
    assert prompt_state.value is None


@test('Any other key adds character at cursor position')
def _(prompt_state=prompt_state):
    prompt_state.value = 'bc'
    prompt_state.cursor_position = 0
    prompt_state = prompt.key_handler(prompt_state, 'a')
    assert prompt_state.value == 'abc'
    assert prompt_state.cursor_position == 1
