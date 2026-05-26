from project.prompts.registry import PromptRegistry


registry = PromptRegistry("project/prompts")

print(registry.list_prompts())

print(
    registry.render(
        "planner",
        question="What in God's name do you want now meatbag?",
        tools="calculator, text_stats, datetime",
    )
)