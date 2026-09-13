import pytest

# Import the module under test and the specific exception it should raise.
# Adjust the import path to match the actual project layout.
from services.policy_client import fetch_policy, PolicyFetchError, cms_client


def test_fetch_policy_raises_on_missing_slug(monkeypatch):
    """If the CMS returns a 404 for the requested slug, fetch_policy must raise.

    The previous implementation caught the error and fell back to
    ``PolicyDoc.empty()`` which let the chat agent answer without any policy
    context. This test patches the underlying CMS client to simulate the 404
    and asserts that the error propagates.
    """

    class MockCMSClient:
        def get_policy(self, slug: str):
            # Simulate the 404 error that occurs after the slug rename.
            raise PolicyFetchError(f"404 Not Found for slug '{slug}'")

    # Replace the real CMS client with the mock that always raises.
    monkeypatch.setattr('services.policy_client.cms_client', MockCMSClient())

    with pytest.raises(PolicyFetchError):
        fetch_policy('refund-policy')
