from .config import settings
from typing import Dict, Any
import random

# --------------------------------------------------------------------
# MOCK LLM (Default)
# --------------------------------------------------------------------
def mock_llm(prompt_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Return deterministic but varied mock responses."""
    user_text = context.get("features", {}).get("user_query") or ""
    canned_responses = [
        "Sure, here's a simplified explanation.",
        "This is a mock response from the inference service.",
        "The model is running in mock mode; no real LLM call was made.",
    ]
    return {
        "response_text": f"[MOCK RESPONSE] {random.choice(canned_responses)}\nPROMPT USED:\n{prompt_text}",
        "trace": "mock_chain_of_thought_hidden",
        "model": "mock-llm"
    }


# --------------------------------------------------------------------
# LLM ROUTER
# --------------------------------------------------------------------
def run_llm(prompt_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch to mock or future real LLM."""
    if settings.LLM_MODE == "mock":
        return mock_llm(prompt_text, context)

    raise NotImplementedError("Only mock mode enabled for now.")
