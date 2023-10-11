from yakh import get_key

from questo.prompt.state import PromptState
from questo.prompt.prompt import Prompt

from questo.prompt.navigation_handlers import prompt_key_handler

prompt = Prompt()
prompt.state = PromptState(title="Enter your name")

with prompt.diplayed():
    while True:
        prompt.state = prompt_key_handler(prompt.state, get_key())
        if prompt.state.exit or prompt.state.abort:
            break
    print(prompt.result)