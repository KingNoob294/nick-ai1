import pytest

from nick_ai.providers.registry import ProviderRegistry


class FakeProvider:
    name = "fake"


def test_registry():
    registry = ProviderRegistry()
    registry.register(FakeProvider())
    assert registry.get("fake").name == "fake"


def test_unknown_provider():
    with pytest.raises(ValueError):
        ProviderRegistry().get("missing")
