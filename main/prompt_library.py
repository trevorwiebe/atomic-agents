from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator

class PromptLibrary:
    
    WEBSITE_DEVELOPER = SystemPromptGenerator(
        background=[
            "You are a website developer that in knowledgable in javascript, html and css.  You provide coding examples and explanations in a clear, simple manner."
        ],
        steps=[
            "Analyze the users question, considering any past history that would influence your response."
        ],
        output_instructions=[
            "Provide code snippets inside triple back ticks, for example ```const foo = 'I love javascript'``` "
        ]
    )

    @staticmethod
    def get_prompt(name):
        return getattr(PromptLibrary, name.upper(), "Prompt not found")