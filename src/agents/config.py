import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    provider: str
    api_key: str
    model_id: str
    max_tokens: int
    temperature: float
    max_steps: int
    share_gradio: bool


def get_settings() -> Settings:
    load_dotenv()
    provider = os.getenv("AGENT_PROVIDER", "gemini").lower()
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to .env or export it in your shell."
            )
        default_model = "gemini/gemini-3.6-flash"
    elif provider == "hf":
        api_key = os.getenv("HF_TOKEN")
        if not api_key:
            raise RuntimeError(
                "HF_TOKEN is not set. Add it to .env or export it in your shell."
            )
        default_model = "Qwen/Qwen2.5-Coder-32B-Instruct"
    else:
        raise ValueError("AGENT_PROVIDER must be either 'gemini' or 'hf'.")

    return Settings(
        provider=provider,
        api_key=api_key,
        model_id=os.getenv("AGENT_MODEL_ID", default_model),
        max_tokens=int(os.getenv("AGENT_MAX_TOKENS", "2096")),
        temperature=float(os.getenv("AGENT_TEMPERATURE", "0.5")),
        max_steps=int(os.getenv("AGENT_MAX_STEPS", "6")),
        share_gradio=os.getenv("GRADIO_SHARE", "false").lower() == "true",
    )
