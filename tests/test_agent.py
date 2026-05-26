from project.agent import QAAgent


def test_meatbag_prompt_uses_text_stats():
    agent = QAAgent()
    action = agent.choose_tool("What in God's name do you want now meatbag?")

    assert action["tool_name"] == "text_stats"


def test_plain_math_uses_calculator():
    agent = QAAgent()
    action = agent.choose_tool("25 * 17")

    assert action["tool_name"] == "calculator"
    assert action["arguments"]["expression"] == "25 * 17"


def test_math_question_extracts_expression():
    agent = QAAgent()
    action = agent.choose_tool("What is 25 * 17?")

    assert action["tool_name"] == "calculator"
    assert action["arguments"]["expression"] == "25 * 17"


def test_time_question_uses_datetime():
    agent = QAAgent()
    action = agent.choose_tool("What is the time?")

    assert action["tool_name"] == "datetime"