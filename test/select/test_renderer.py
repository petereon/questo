from questo import select
from ward import test, fixture


@fixture
def select_state():
    return select.SelectState(
        title='Select a number',
        options=[str(i) for i in range(6)],
        index=0,
        pagination=False,
        page_size=5,
        select_multiple=False,
    )


@test('DefaultRenderer renders state with 6 options, no pagination and no multiple selection')
def _(state=select_state):
    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
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


@test('DefaultRenderer renders state with 6 options, second option selected no pagination and no multiple selection')
def _(state=select_state):
    state.index = 1
    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
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


@test('DefaultRenderer renders state with 6 options, page size 5 and no multiple selection')
def _(state=select_state):
    state.index = 1
    state.page_size = 5
    state.pagination = True
    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
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


@test('DefaultRenderer renders state with 6 options, page size 5 with cursor on 6th option and no multiple selection')
def _(state=select_state):
    state.index = 5
    state.page_size = 5
    state.pagination = True
    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
    assert (
        rendered
        == '''[bold]Select a number[/bold]
[bold cyan1]>[/bold cyan1] 5





◦•
'''
    )


@test('DefaultRenderer renders state with 6 options, and multiple selection no options selected')
def _(state=select_state):
    state.index = 0
    state.select_multiple = True

    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
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


@test('DefaultRenderer renders state with 6 options, and multiple selection no options selected')
def _(state=select_state):
    state.index = 1
    state.selected_indexes = [0, 2]
    state.select_multiple = True

    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
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


@test('DefaultRenderer renders state with 6 options and only some filtered')
def _(state=select_state):
    state.index = 1
    state.filter = '1'

    renderer = select.DefaultRenderer()
    rendered = renderer.render(state)
    assert (
        rendered
        == '''[bold]Select a number[/bold] [grey35]1[/grey35]
[bold cyan1]>[/bold cyan1] [bold]1[/bold]





'''
    )


@test('DefaultRenderer renders state with 6 options, no pagination and no multiple selection')
def _(state=select_state):
    renderer = select.DefaultRenderer()
    state.error = 'Something\'s wrong'
    rendered = renderer.render(state)
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
