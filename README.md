# Questo

**Questo** is not your ordinary library of CLI elements; It's a framework. It's modular, extensible, Pythonic and brain friendly. You can build your own CLI elements, with custom key-press handling, validation and rendering, all in plain old Python; No magic.

## Basic Usage

```python
from questo import select, prompt
from yakh import get_key


selector = select.Select()
selector.state = select.SelectState(
    title="Who's your favorite Teletubbie", 
    options=["Tinky Winky", "Dipsy", "Laa-Laa", "Po", "The Weird Vacuum Thing"], 
    selected=4
)

with selector.displayed():
    while True:
        selector.state = select.key_handler(selector.state, get_key())
        if selector.state.exit or selector.state.abort:
            break

prompter = prompt.Prompt()
prompter.state = prompt.PromptState(
    title=f"Why {selector.result}?", 
)

with prompter.displayed():
    while True:
        prompter.state = prompt.key_handler(prompter.state, get_key())
        if prompter.state.exit or prompter.state.abort:
            break

print(f"Ah, of course: {prompter.result}")
```
