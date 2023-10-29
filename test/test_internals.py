from ward import test


@test('Style can be applied to a string')
def _():
    from questo.internals import _apply_style

    assert _apply_style('test', 'bold') == '[bold]test[/bold]'


@test('Style can be parsed from string')
def _():
    from questo.internals import _parse_string_style
    from rich.style import Style

    assert _parse_string_style('bold') == Style.parse('bold')
