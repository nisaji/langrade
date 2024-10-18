import os
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import pytest
from unittest.mock import patch, AsyncMock
from dotenv import load_dotenv
from langrade.providers import LLMProviderFactory, LLMProvider
from langrade.constants import DEFAULT_MODEL

# 環境変数を読み込む
load_dotenv()


@pytest.fixture
def api_keys():
    return {
        "openai": os.getenv("OPENAI_API_KEY"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
    }


@pytest.fixture
def models():
    return {
        "openai": os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        "anthropic": os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229"),
        "google": os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest"),
        "groq": os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", ["openai", "anthropic", "google", "groq"])
async def test_provider_creation(api_keys, models, provider):
    api_key = api_keys[provider]
    model = models[provider]

    if not api_key:
        pytest.skip(f"API key for {provider} not found in environment variables")

    provider_instance = LLMProviderFactory.create_provider(provider, api_key, model)
    assert isinstance(provider_instance, LLMProvider)


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", ["openai", "anthropic", "google", "groq"])
async def test_provider_generation(api_keys, models, provider):
    api_key = api_keys[provider]
    model = models[provider]

    if not api_key:
        pytest.skip(f"API key for {provider} not found in environment variables")

    provider_instance = LLMProviderFactory.create_provider(provider, api_key, model)

    test_prompt = "What is the capital of France?"
    response = await provider_instance.agenerate(test_prompt)

    assert isinstance(response, str)
    assert len(response) > 0
    assert "Paris" in response


@pytest.mark.asyncio
async def test_invalid_provider():
    with pytest.raises(ValueError):
        LLMProviderFactory.create_provider(
            "invalid_provider", "dummy_key", "dummy_model"
        )


@pytest.mark.asyncio
@patch("langrade.providers.ChatOpenAI")
async def test_openai_provider_mock(mock_chat):
    mock_llm = AsyncMock(spec=ChatOpenAI)
    mock_llm.ainvoke.return_value = AsyncMock(content="Mocked response")
    mock_chat.return_value = mock_llm

    provider = LLMProviderFactory.create_provider("openai", "fake_api_key")
    result = await provider.agenerate("Test prompt")

    assert result == "Mocked response"


@pytest.mark.asyncio
@patch("langrade.providers.ChatAnthropic")
async def test_anthropic_provider_mock(mock_chat):
    mock_llm = AsyncMock(spec=ChatAnthropic)
    mock_llm.ainvoke.return_value = AsyncMock(content="Mocked response")
    mock_chat.return_value = mock_llm

    provider = LLMProviderFactory.create_provider("anthropic", "fake_api_key")
    result = await provider.agenerate("Test prompt")

    assert result == "Mocked response"


@pytest.mark.asyncio
@patch("langrade.providers.ChatGoogleGenerativeAI")
async def test_google_provider_mock(mock_chat):
    mock_llm = AsyncMock(spec=ChatGoogleGenerativeAI)
    mock_llm.ainvoke.return_value = AsyncMock(content="Mocked response")
    mock_chat.return_value = mock_llm

    provider = LLMProviderFactory.create_provider("google", "fake_api_key")
    result = await provider.agenerate("Test prompt")

    assert result == "Mocked response"


@pytest.mark.asyncio
@patch("langrade.providers.ChatGroq")
async def test_groq_provider_mock(mock_chat):
    mock_llm = AsyncMock(spec=ChatGroq)
    mock_llm.ainvoke.return_value = AsyncMock(content="Mocked response")
    mock_chat.return_value = mock_llm

    provider = LLMProviderFactory.create_provider("groq", "fake_api_key")
    result = await provider.agenerate("Test prompt")

    assert result == "Mocked response"
    mock_chat.assert_called_once()
