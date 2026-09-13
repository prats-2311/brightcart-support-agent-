import pytest
import requests

# Import the module under test – adjust the import path as needed for your project structure
from policy_client import get_policy, PolicyFetchError


def test_get_policy_raises_on_404(monkeypatch):
    """PolicyClient must raise PolicyFetchError on a 404 instead of returning an empty dict."""

    class DummyResponse:
        status_code = 404

        def raise_for_status(self):
            # Simulate the behaviour of requests.Response.raise_for_status() for 404
            raise requests.HTTPError(response=self)

        def json(self):
            return {}

    def fake_get(*args, **kwargs):
        return DummyResponse()

    # Patch the internal requests.get used by policy_client
    monkeypatch.setattr('policy_client.requests.get', fake_get)

    # The call should now raise PolicyFetchError rather than silently returning an empty policy
    with pytest.raises(PolicyFetchError):
        get_policy('refund-policy')
