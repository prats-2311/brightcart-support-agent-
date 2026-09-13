import pytest
from services import policy_client

def test_fetch_policy_raises_on_missing_slug(monkeypatch):
    """PolicyClient should raise PolicyFetchError for a 404 slug instead of returning an empty document."""

    class DummyCMSClient:
        def fetch(self, slug):
            # Simulate a 404 response from the CMS.
            raise policy_client.PolicyFetchError(f"404 Not Found for slug: {slug}")

    # Patch the CMSClient used inside policy_client to our dummy implementation.
    monkeypatch.setattr(policy_client, "CMSClient", DummyCMSClient)

    with pytest.raises(policy_client.PolicyFetchError):
        policy_client.fetch_policy("refund-policy")
