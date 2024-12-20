from questo.internals import _apply_style, _parse_string_style
from rich.style import Style


def test_apply_style():
    assert _apply_style('test', 'bold') == '[bold]test[/bold]'


def test_parse_string_style():
    assert _parse_string_style('bold') == Style.parse('bold')
