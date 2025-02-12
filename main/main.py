import os
import instructor
import openai

from rich.console import Console
from rich.text import Text

from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig, BaseAgentInputSchema, BaseAgentOutputSchema
from prompt_library import PromptLibrary
from get_code_changes import CodeChangesProvider

API_KEY = os.getenv("API_KEY")
SELECTED_LIBRARY_PROMPT = "WEBSITE_DEVELOPER" # change this to what ever prompt best fits the task at hand

console = Console()

client = instructor.from_openai(openai.OpenAI(api_key=API_KEY))

promptLibrary = PromptLibrary(
    code_base_file="/Users/trevorwiebe/Documents/WebApps/sunny-slope-llc/website",
    ignore_path="/Users/trevorwiebe/Documents/WebApps/sunny-slope-llc/agent"
)

agent = BaseAgent(
    config=BaseAgentConfig(
        client=client, 
        model="gpt-4o-mini"
    ),
)

commitMessageAgent = BaseAgent(
    config=BaseAgentConfig(
        client=client,
        model="gpt-4o-mini",
    )
)


# Add initial message to agent memory and print it
initial_message = "Hello, how can I help you today?"
agent.memory.add_message("assistant", content=BaseAgentOutputSchema(chat_message=initial_message))

# Print initial message
console.print(Text(f"Assistant: {initial_message}", style="bold green"))

while True:

    # Get the user input
    user_input = console.input("You: ")

    if user_input == "cma":
        commitMessageAgent.system_prompt_generator = promptLibrary.get_prompt("COMMIT_MESSAGE_HELPER")
        commitMessageResponse = commitMessageAgent.run(BaseAgentInputSchema(chat_message="Please create a commit messages for me based on the code changes."))
        console.print(Text(f"Commit Message Assistant:\n{commitMessageResponse.chat_message}", style="bold blue"))
    else:
        agent.system_prompt_generator = promptLibrary.get_prompt(SELECTED_LIBRARY_PROMPT)
        response = agent.run(BaseAgentInputSchema(chat_message=user_input))
        console.print(Text(f"Assistant: {response.chat_message}", style="bold green"))