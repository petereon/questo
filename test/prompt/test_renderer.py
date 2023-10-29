from ward import test
from questo import prompt


@test('Prompt state with title, value, 0 cursor positions and no error renders')
def _():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value')
    assert (
        selector.renderer(selector.state) == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] [black on white]T[/black on white]est value \n'
    )


@test('Prompt state with title, value, 1 cursor position and no error renders')
def _():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value', cursor_position=1)
    assert (
        selector.renderer(selector.state) == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] T[black on white]e[/black on white]st value \n'
    )


@test('Prompt state with title, value, 0 cursor positions and error renders')
def _():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value', error='Test error')
    assert (
        selector.renderer(selector.state)
        == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] [black on white]T[/black on white]est value \n[red]Test error[/red]\n'
    )


@test('Prompt state with title, value, 0 cursor positions, error and completion options renders')
def _():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(
        title='test',
        value='Test value',
        error='Test error',
        completion=prompt.CompletionState(options=['test1', 'test2'], index=0, in_completion_ctx=True),
    )
    assert (
        selector.renderer(selector.state)
        == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] [black on white]T[/black on white]est value \n[red]Test error[/red]\n[black on white]test1[/black on white] test2'
    )


@test('Prompt state with title, value, 0 cursor positions, error and completion options renders')
def _():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(
        title='test',
        value='Test value',
        error='Test error',
        completion=prompt.CompletionState(options=['test1', 'test2'], index=1, in_completion_ctx=True),
    )
    assert (
        selector.renderer(selector.state)
        == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] [black on white]T[/black on white]est value \n[red]Test error[/red]\ntest1 [black on white]test2[/black on white]'
    )
