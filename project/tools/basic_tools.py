from datetime import datetime
from zoneinfo import ZoneInfo

from project.tools.registry import register_tool
from project.tools.params_models import (
    CalculatorParams,
    DateTimeParams,
    TextStatsParams,
)


@register_tool(
    name="calculator",
    description="Evaluates simple arithmetic expressions.",
    params_model=CalculatorParams,
)
def calculator(params: CalculatorParams) -> str:
    allowed_chars = set("0123456789+-*/(). %")

    if not set(params.expression).issubset(allowed_chars):
        return "Error: expression contains unsupported characters."

    try:
        result = eval(params.expression, {"__builtins__": {}})
        return str(result)
    except Exception as error:
        return f"Error while calculating: {error}"


@register_tool(
    name="datetime",
    description="Returns the current date and time.",
    params_model=DateTimeParams,
)
def current_datetime(params: DateTimeParams) -> str:
    try:
        if params.timezone:
            now = datetime.now(ZoneInfo(params.timezone))
        else:
            now = datetime.now()

        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as error:
        return f"Error while getting datetime: {error}"


@register_tool(
    name="text_stats",
    description="Counts characters, words, and sentences in a piece of text.",
    params_model=TextStatsParams,
)
def text_stats(params: TextStatsParams) -> str:
    text = params.text.strip()

    words = text.split()
    sentences = text.count(".") + text.count("!") + text.count("?")

    return (
        f"Characters: {len(text)}\n"
        f"Words: {len(words)}\n"
        f"Sentences: {sentences}"
    )