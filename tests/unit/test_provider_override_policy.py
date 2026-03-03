from src.archi.providers.base import ProviderType
from src.interfaces.chat_app.app import (
    _is_provider_enabled_in_config,
    _validate_default_provider_enabled,
)


def test_provider_override_blocked_when_explicitly_disabled():
    config = {
        "services": {
            "chat_app": {
                "providers": {
                    "local": {"enabled": False},
                }
            }
        }
    }

    enabled, reason = _is_provider_enabled_in_config(config, ProviderType.LOCAL)
    assert enabled is False
    assert "disabled" in (reason or "").lower()


def test_provider_override_allowed_when_provider_block_missing():
    config = {
        "services": {
            "chat_app": {
                "providers": {}
            }
        }
    }

    enabled, reason = _is_provider_enabled_in_config(config, ProviderType.LOCAL)
    assert enabled is True
    assert reason is None


def test_default_provider_validation_rejects_disabled_default():
    config = {
        "services": {
            "chat_app": {
                "default_provider": "local",
                "providers": {
                    "local": {"enabled": False},
                },
            }
        }
    }

    try:
        _validate_default_provider_enabled(config)
    except ValueError as exc:
        assert "default_provider" in str(exc)
    else:
        raise AssertionError("Expected ValueError for disabled default provider")
