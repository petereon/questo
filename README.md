# Questo

> A library of extensible and modular CLI prompt elements

---

[![CI](https://github.com/petereon/questo/actions/workflows/python-test.yml/badge.svg)](https://github.com/petereon/questo/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/gh/petereon/questo/branch/master/graph/badge.svg)](https://codecov.io/gh/petereon/questo)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/questo?color=g&label=%F0%9F%93%A5%20Downloads)](https://pypi.org/project/questo/)

## Overview

**Questo** provides a set of modular and extensible CLI elements. Unlike other libraries that provide ready-made functions, Questo exposes the internal state and event loop, allowing for complete customization of behavior and rendering.

| Element | Functionality |
|:---|:---|
| `Prompt` | Text input with support for completions and cursor navigation |
| `Select` | List selection with support for single/multi-select, filtering, and pagination |

## Installation

From PyPI:

```sh
pip install questo
```

Using Poetry:

```sh
poetry add questo
```

## Usage

Questo elements are designed to be used within your own event loop. This gives you full control over how keys are handled and how the element is rendered.

### Architecture

Each element in Questo consists of three main components:

1.  **State**: A dataclass that holds the current state of the element (e.g., current value, cursor position, selected index).
2.  **Element**: A class that wraps the state and handles the display context.
3.  **Key Handler**: A function that takes the current state and a keypress, returning a new state.
4.  **Renderer**: A function that takes the current state and returns a string representation to be shown in terminal.

### Example

Here is a complete example showing how to use `Prompt` and `Select` elements.

```python
from yakh import get_key
from questo import prompt, select

# --- Prompt Example ---

# 1. Instantiate the element
name_prompt = prompt.Prompt()

# 2. Initialize the state
name_prompt.state = prompt.PromptState(title="What is your name?")

# 3. Run the event loop
with name_prompt.displayed():
    while True:
        # Get keypress
        key = get_key()
        
        # Update state based on keypress
        name_prompt.state = prompt.key_handler(name_prompt.state, key)
        
        # Check for exit or abort conditions
        if name_prompt.state.exit or name_prompt.state.abort:
            break

# 4. Get the result
name = name_prompt.result

if name:
    print(f"Hello, {name}!")

# --- Select Example ---

# 1. Instantiate the element
color_select = select.Select()

# 2. Initialize the state
color_select.state = select.SelectState(
    title="Choose a color:",
    options=["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan"],
    page_size=3,
    pagination=True
)

# 3. Run the event loop
with color_select.displayed():
    while True:
        key = get_key()
        color_select.state = select.key_handler(color_select.state, key)
        if color_select.state.exit or color_select.state.abort:
            break

# 4. Get the result
color_index = color_select.result
if color_index is not None:
    print(f"You chose: {color_select.state.options[color_index]}")
```

## Customization

Because Questo exposes the state and renderer, you can easily customize the appearance and behavior.

### Custom Renderer

You can provide a custom renderer function to change how the element looks.

```python
from questo import prompt

def my_custom_renderer(state: prompt.PromptState) -> str:
    return f"[bold green]{state.title}[/bold green]\n> {state.value}"

p = prompt.Prompt(renderer=my_custom_renderer)
```

### Custom Key Handler

You can wrap or replace the default key handler to add custom key bindings.

```python
from questo import prompt
from yakh.key import Keys

def my_key_handler(state, key):
    if key == Keys.TAB:
        state.value = "TAB pressed!"
        return state
    return prompt.key_handler(state, key)
```

## Contributing

To start development you can clone the repository:

```sh
git clone https://github.com/petereon/questo.git
```

Change the directory to the project directory:

```sh
cd ./questo/
```

This project uses [`poetry`](https://python-poetry.org/) as a dependency manager. You can install the dependencies using:

```sh
poetry install
```

For testing, this project relies on pytest.

```sh
poetry run poe test
```

## License

The project is licensed under the [MIT License](https://raw.githubusercontent.com/petereon/questo/master/LICENSE).
