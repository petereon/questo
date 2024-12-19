import pytest
from questo import select


@pytest.fixture
def select_state():
    return select.SelectState(
        title='Select a number',
        options=[str(i) for i in range(6)],
        index=0,
        pagination=False,
        page_size=5,
        select_multiple=False,
    )


def test_default_renderer_renders_state_with_6_options_no_pagination_no_multiple_selection(select_state):
    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
[bold cyan1]>[/bold cyan1] 0
  1
  2
  3
  4
  5
'''
    )


def test_default_renderer_renders_state_with_6_options_second_option_selected_no_pagination_no_multiple_selection(select_state):
    select_state.index = 1
    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
  0
[bold cyan1]>[/bold cyan1] 1
  2
  3
  4
  5
'''
    )


def test_default_renderer_renders_state_with_6_options_page_size_5_no_multiple_selection(select_state):
    select_state.index = 1
    select_state.page_size = 5
    select_state.pagination = True
    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
  0
[bold cyan1]>[/bold cyan1] 1
  2
  3
  4

•◦
'''
    )


def test_default_renderer_renders_state_with_6_options_page_size_5_cursor_on_6th_option_no_multiple_selection(select_state):
    select_state.index = 5
    select_state.page_size = 5
    select_state.pagination = True
    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
[bold cyan1]>[/bold cyan1] 5





◦•
'''
    )


def test_default_renderer_renders_state_with_6_options_multiple_selection_no_options_selected(select_state):
    select_state.index = 0
    select_state.select_multiple = True

    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
[bold cyan1]>[/bold cyan1]   0
    1
    2
    3
    4
    5
'''
    )


def test_default_renderer_renders_state_with_6_options_multiple_selection_some_options_selected(select_state):
    select_state.index = 1
    select_state.selected_indexes = [0, 2]
    select_state.select_multiple = True

    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
  [green]✓[/green] 0
[bold cyan1]>[/bold cyan1]   1
  [green]✓[/green] 2
    3
    4
    5
'''
    )


def test_default_renderer_renders_state_with_6_options_some_filtered(select_state):
    select_state.index = 1
    select_state.filter = '1'

    renderer = select.DefaultRenderer()
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold] [grey35]1[/grey35]
[bold cyan1]>[/bold cyan1] [bold]1[/bold]





'''
    )


def test_default_renderer_renders_state_with_6_options_no_pagination_no_multiple_selection_with_error(select_state):
    renderer = select.DefaultRenderer()
    select_state.error = 'Something\'s wrong'
    rendered = renderer.render(select_state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
[bold cyan1]>[/bold cyan1] 0
  1
  2
  3
  4
  5
[red]Something's wrong[/red]
'''
    )
