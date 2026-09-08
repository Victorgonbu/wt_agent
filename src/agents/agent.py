from smolagents import CodeAgent, InferenceClientModel, LiteLLMModel

from agents.config import Settings
from agents.tools import build_tools


def build_agent(settings: Settings) -> CodeAgent:
    """Build a CodeAgent using the current smolagents API."""
    if settings.provider == "gemini":
        model = LiteLLMModel(
            model_id=settings.model_id,
            api_key=settings.api_key,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
        )
    else:
        model = InferenceClientModel(
            model_id=settings.model_id,
            token=settings.api_key,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
        )
    agent = CodeAgent(
        model=model,
        tools=build_tools(),
        max_steps=settings.max_steps,
        verbosity_level=1,
    )

    return agent
