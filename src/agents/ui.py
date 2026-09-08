from smolagents import GradioUI

from agents.agent import build_agent
from agents.config import get_settings


def launch() -> None:
    """Build and launch the local Gradio interface."""
    settings = get_settings()
    agent = build_agent(settings)
    GradioUI(agent).launch(share=settings.share_gradio)
