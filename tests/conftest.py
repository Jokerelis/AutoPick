import pytest


@pytest.fixture(autouse=True)
def disable_real_ai(monkeypatch):
    monkeypatch.setenv("AUTOPICK_AI_ENABLED", "false")