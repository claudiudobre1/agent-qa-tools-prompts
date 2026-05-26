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


def test_answer_returns_calculator_result():
    agent = QAAgent()
    answer = agent.answer("25 * 17")

    assert "Tool used: calculator" in answer
    assert "Result: 425" in answer


def test_debug_answer_contains_react_trace():
    agent = QAAgent()
    answer = agent.answer("25 * 17", debug=True)

    assert "REACT TRACE:" in answer
    assert "Act 1: Call tool 'calculator'" in answer
    assert "Observe 1: 425" in answer
    assert "FINAL ANSWER:" in answer