import os
import instructor
import openai

from rich.console import Console
from rich.text import Text

from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig, BaseAgentInputSchema, BaseAgentOutputSchema
from prompt_library import PromptLibrary

API_KEY = os.getenv("API_KEY")

console = Console()

client = instructor.from_openai(openai.OpenAI(api_key=API_KEY))

prompt = PromptLibrary.get_prompt("WEBSITE_DEVELOPER")

agent = BaseAgent(
    config=BaseAgentConfig(
        client=client, 
        model="gpt-4o-mini",
        system_prompt_generator=prompt
    ),
)

# Add initial message to agent memory and print it
initial_message = "Hello, how can I help you today?"
agent.memory.add_message("assistant", content=BaseAgentOutputSchema(chat_message=initial_message))

# Print initial message
console.print(Text(f"Assistant: {initial_message}", style="bold green"))

while True:

    # Get the user input
    user_input = console.input("You: ")

    response = agent.run(BaseAgentInputSchema(chat_message=user_input))

    console.print(Text(f"Assistant: {response.chat_message}", style="bold green"))