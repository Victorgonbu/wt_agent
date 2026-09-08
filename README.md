# Agents

A modular [smolagents](https://github.com/huggingface/smolagents)
`CodeAgent` with a Gradio chat interface, Gemini support, web search, current
weather, and timezone tools.

## Features

- Gemini inference through LiteLLM, enabled by default.
- Hugging Face inference as an optional provider.
- Current weather lookup through the keyless Open-Meteo API.
- DuckDuckGo web search for current or external information.
- Current local time lookup for IANA timezones.
- Gradio interface with streamed agent steps.
- Environment-based configuration with `.env` support.

## Requirements

- Python 3.14 or newer
- [`uv`](https://docs.astral.sh/uv/)
- A Gemini API key or Hugging Face access token

## Setup

Install and synchronize the project dependencies:

```bash
uv sync
```

Create a `.env` file in the project root. Gemini is the default provider:

```env
AGENT_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
```

Start the application:

```bash
uv run agents
```

The Gradio interface runs locally by default. Set `GRADIO_SHARE=true` only when
you need a temporary public Gradio URL:

```env
GRADIO_SHARE=true
```

## Providers

### Gemini

Gemini is the default provider and uses LiteLLM through `smolagents`:

```env
AGENT_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
# Optional override
AGENT_MODEL_ID=gemini/gemini-3.6-flash
```

### Hugging Face

To use Hugging Face instead:

```env
AGENT_PROVIDER=hf
HF_TOKEN=your_hugging_face_token
# Optional override
AGENT_MODEL_ID=Qwen/Qwen2.5-Coder-32B-Instruct
```

The provider is selected in `src/agents/config.py`. Both providers use the
same tools and agent configuration.

## Configuration

The following environment variables are supported:

| Variable | Default | Purpose |
| --- | --- | --- |
| `AGENT_PROVIDER` | `gemini` | Inference provider: `gemini` or `hf` |
| `AGENT_MODEL_ID` | Provider-specific | Model identifier |
| `GEMINI_API_KEY` | None | Gemini API credential |
| `HF_TOKEN` | None | Hugging Face credential |
| `AGENT_MAX_TOKENS` | `2096` | Maximum generated tokens |
| `AGENT_TEMPERATURE` | `0.5` | Model sampling temperature |
| `AGENT_MAX_STEPS` | `6` | Maximum agent execution steps |
| `GRADIO_SHARE` | `false` | Create a temporary public Gradio link |

## Project structure

```text
src/
├── main.py              # Script entry point
└── agents/
	├── agent.py         # Model and CodeAgent construction
	├── config.py        # Environment-backed settings
	├── tools.py         # Weather, search, time, and final-answer tools
	└── ui.py            # Gradio application launcher
```

The console script configured in `pyproject.toml` is `agents`, so these commands
are equivalent:

```bash
uv run agents
uv run python src/main.py
```

## Security

- Never commit `.env` or place API keys directly in source code.
- `.env` is ignored by Git through `.gitignore`.
- If a key is exposed in a chat, terminal output, commit, or screenshot, revoke
	it and generate a replacement before continuing.
- Do not enable `GRADIO_SHARE` unless you intend to expose the interface through
	a temporary public URL.

## Troubleshooting

If the application reports a missing credential, check that `.env` is in the
project root and that its variable matches the selected provider:

```bash
AGENT_PROVIDER=gemini  # requires GEMINI_API_KEY
AGENT_PROVIDER=hf      # requires HF_TOKEN
```

If a provider rejects the configured model, set a currently available model in
`AGENT_MODEL_ID`. The agent and tools do not need to change when switching
providers.
