from src.utils.provider_config_validation import (
    get_disabled_default_provider_reason,
    is_provider_enabled_in_config,
)


def test_provider_enabled_when_missing_block():
    config = {"services": {"chat_app": {"default_provider": "local"}}}
    enabled, reason = is_provider_enabled_in_config(config, "local")
    assert enabled is True
    assert reason is None


def test_provider_disabled_when_enabled_false():
    config = {
        "services": {
            "chat_app": {
                "providers": {
                    "local": {
                        "enabled": False,
                    }
                }
            }
        }
    }
    enabled, reason = is_provider_enabled_in_config(config, "local")
    assert enabled is False
    assert "services.chat_app.providers.local.enabled" in str(reason)


def test_default_provider_disabled_reason():
    config = {
        "services": {
            "chat_app": {
                "default_provider": "local",
                "providers": {
                    "local": {
                        "enabled": False,
                    }
                },
            }
        }
    }
    reason = get_disabled_default_provider_reason(config)
    assert reason is not None
    assert "services.chat_app.providers.local.enabled" in reason

