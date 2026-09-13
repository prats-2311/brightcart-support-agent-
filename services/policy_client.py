"""Policy document client for the Brightcart support agent."""

import httpx

CMS_BASE_URL = "https://cms.brightcart.internal"


class PolicyFetchError(Exception):
    """Raised when the policy document cannot be retrieved.

    Callers MUST NOT catch this and proceed as if no restrictions apply.
    The correct response is to decline to answer and escalate to a human.
    """


def fetch_policy(slug: str = "refunds-policy") -> list:
    """Fetch a policy document from the CMS by slug.

    Fails closed: raises PolicyFetchError on any failure instead of
    returning an empty list, so callers can never mistake "unknown" for
    "no restrictions apply".
    """
    resp = httpx.get(f"{CMS_BASE_URL}/policies/{slug}", timeout=5.0)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise PolicyFetchError(f"policy fetch failed for slug={slug!r}: {exc}") from exc
    return resp.json()
