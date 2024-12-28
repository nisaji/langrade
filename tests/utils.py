import os
import json
from typing import Optional, Dict, Any


def load_env_config() -> Dict[str, Any]:
    """Load and return all environment configurations"""
    return {
        "provider": os.getenv("DEFAULT_ENGINE_TYPE", "openai"),
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": os.getenv("OPENAI_MODEL"),
        },
        "anthropic": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": os.getenv("CLAUDE_MODEL"),
        },
        "vertexai": {
            "model": os.getenv("GEMINI_MODEL"),
            "credentials": _load_vertex_credentials(),
        },
    }


def _load_vertex_credentials() -> Optional[Dict[str, Any]]:
    """Load VertexAI credentials from the specified path"""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path or not os.path.exists(credentials_path):
        return None

    try:
        with open(credentials_path) as f:
            return json.load(f)
    except Exception:
        return None


def get_provider_credentials(provider: str) -> tuple[Optional[str], Optional[str]]:
    """Get API key and model for specified provider"""
    config = load_env_config()
    provider_config = config.get(provider, {})

    if provider == "vertexai":
        return provider_config.get("credentials"), provider_config.get("model")
    return provider_config.get("api_key"), provider_config.get("model")
