import pytest
from questo import prompt

def test_prompt_state_with_title_value_0_cursor_positions_and_no_error_renders():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value')
    assert (
        selector.renderer(selector.state) == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] [black on white]T[/black on white]est value \n'
    )

def test_prompt_state_with_title_value_1_cursor_position_and_no_error_renders():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value', cursor_position=1)
    assert (
        selector.renderer(selector.state) == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] T[black on white]e[/black on white]st value \n'
    )

def test_prompt_state_with_title_value_0_cursor_positions_and_error_renders():
    selector = prompt.Prompt()
    selector.state = prompt.PromptState(title='test', value='Test value', error='Test error')
    assert (
        selector.renderer(selector.state)
        == '[bold]test [/bold]\n[bold cyan1]>[/bold cyan1] [black on white]T[/black on white]est value \n[red]Test error[/red]\n'
    )

def test_prompt_state_with_title_value_0_cursor_positions_error_and_completion_options_renders_index_0():
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

def test_prompt_state_with_title_value_0_cursor_positions_error_and_completion_options_renders_index_1():
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
