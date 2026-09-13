import pytest
from unittest import mock

# Import the function under test and the expected exception.
from services.policy_client import fetch_policy, PolicyFetchError

def test_fetch_policy_raises_on_404(monkeypatch):
    """fetch_policy must raise PolicyFetchError when CMS returns 404 instead of
    silently returning an empty policy document."""
    # Create a mock response that mimics requests.Response for a 404.
    class MockResponse:
        status_code = 404
        def raise_for_status(self):
            raise Exception("404 Client Error: Not Found for url")
        def json(self):
            return {}

    # Mock the internal HTTP call used by fetch_policy. Assume fetch_policy uses `requests.get`.
    monkeypatch.setattr("services.policy_client.requests.get", lambda url, **kw: MockResponse())

    with pytest.raises(PolicyFetchError):
        fetch_policy("refund-policy")
