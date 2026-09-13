"""Policy document client for the Brightcart support agent."""

import httpx

CMS_BASE_URL = "https://cms.brightcart.internal"


def fetch_policy(slug: str = "refund-policy") -> list:
    """Fetch a policy document from the CMS by slug.

    Returns the raw policy document list, or an empty list if the document
    cannot be found. Callers must treat an empty list as "policy unknown",
    never as "no restrictions apply".
    """
    try:
        resp = httpx.get(f"{CMS_BASE_URL}/policies/{slug}", timeout=5.0)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError:
        # TODO: should this raise instead of silently returning empty?
        return []
