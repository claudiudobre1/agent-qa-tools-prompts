import re

from project.guardrails.models import GuardrailResult


MAX_QUERY_LENGTH = 1000

BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"disregard previous instructions",
    r"reveal.*system prompt",
    r"show.*system prompt",
    r"developer message",
    r"hidden prompt",
    r"bypass safety",
    r"jailbreak",
    r"act as dan",
]


def validate_query(query: str) -> GuardrailResult:
    if not isinstance(query, str):
        return GuardrailResult(
            allowed=False,
            reason="Query must be a string.",
        )

    cleaned_query = query.strip()

    if not cleaned_query:
        return GuardrailResult(
            allowed=False,
            reason="Query cannot be empty.",
        )

    if len(cleaned_query) > MAX_QUERY_LENGTH:
        return GuardrailResult(
            allowed=False,
            reason=f"Query is too long. Maximum length is {MAX_QUERY_LENGTH} characters.",
        )

    lowered_query = cleaned_query.lower()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, lowered_query):
            return GuardrailResult(
                allowed=False,
                reason="Possible prompt injection detected.",
            )

    return GuardrailResult(
        allowed=True,
        reason="Query passed guardrail validation.",
    )