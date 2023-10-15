# questo

> Introducing **Questo**: The CLI Library Redefining Your Command Line Experience

**Questo** is not your ordinary library of CLI elements; it's a framework designed with modularity, customization, composability, and reactivity at its core. **Questo** puts you into the driver seat of your CLI experience, allowing you to create a CLI that is uniquely yours. No holds barred.

🧩 **Modularity Redefined:** Mix and match different keypress-handlers and renderers of your making to effortlessly create the CLI experience that perfectly suits your needs. Adaptability at its finest!

⌨️ **User-Defined Control:** Define your keypress handlers to react precisely as you desire. Empower your CLI to respond to user input in ways that make sense for your specific application. Do you want `vim`-like navigation? WASD? Arrow keys? The choice is yours.

🎨 **Render Your Way:** With **Questo**, you hold the brush. Design your CLI's appearance with custom renderers. Take state, transform to `str` and **Questo** will take care of the rest. It's that easy!

🔄 **Reactive Magic:** Witness your CLI come to life with reactive rendering. **Questo** ensures that your interface dynamically responds to state changes in real-time, all while affording you the fine grained control of the state. Say goodbye to static, dull command line applications, and hello to an engaging, responsive interaction.

🧠 **Brain Friendly:** **Questo** is designed to be Pythonic - easy to use, easy to understand, and easy to extend. It's the CLI library that you can actually wrap your head around without having to read a novel.

Discover a library that combines modularity, customization and reactivity to give you unprecedented control over your CLI, all while remaining familiar and friendly.


## Example

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
