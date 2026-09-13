import pytest
from unittest.mock import patch

from services.policy_client import fetch_policy, PolicyFetchError


def test_fetch_policy_raises_when_slug_missing():
    """fetch_policy must fail loudly if the requested slug does not exist.
    The previous implementation swallowed the 404 and returned an empty
    PolicyDoc, allowing the chat agent to hallucinate policy details. This
    test patches the CMS client to raise a 404‑like exception and asserts that
    fetch_policy propagates a PolicyFetchError.
    """
    with patch('services.policy_client.CMSClient') as MockClient:
        mock_instance = MockClient.return_value
        # Simulate CMS returning a 404 error for the slug
        mock_instance.get_policy.side_effect = Exception('404 Not Found')
        with pytest.raises(PolicyFetchError):
            fetch_policy('refund-policy')
