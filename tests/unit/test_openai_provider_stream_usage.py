from unittest.mock import patch

from src.archi.providers.base import ProviderConfig, ProviderType
from src.archi.providers.openai_provider import OpenAIProvider


def test_openai_provider_enables_stream_usage_by_default():
    config = ProviderConfig(
        provider_type=ProviderType.OPENAI,
        api_key_env="",
        extra_kwargs={},
    )
    provider = OpenAIProvider(config)

    with patch("src.archi.providers.openai_provider.ChatOpenAI") as mock_chat:
        provider.get_chat_model("gpt-4o-mini")
        kwargs = mock_chat.call_args.kwargs
        assert kwargs["streaming"] is True
        assert kwargs["stream_options"] == {"include_usage": True}


def test_openai_provider_merges_stream_options_with_include_usage():
    config = ProviderConfig(
        provider_type=ProviderType.OPENAI,
        api_key_env="",
        extra_kwargs={"stream_options": {"foo": "bar"}},
    )
    provider = OpenAIProvider(config)

    with patch("src.archi.providers.openai_provider.ChatOpenAI") as mock_chat:
        provider.get_chat_model(
            "gpt-5",
            stream_options={"include_usage": False, "baz": 1},
        )
        kwargs = mock_chat.call_args.kwargs
        assert kwargs["stream_options"] == {
            "include_usage": False,
            "foo": "bar",
            "baz": 1,
        }
