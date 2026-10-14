# Hand-written: scripts/patch_generated.py makes each list method use this.

from __future__ import annotations

import typing
from urllib.parse import parse_qs, urlsplit


def page_token(next_page_url: typing.Optional[str]) -> typing.Optional[str]:
    """Returns the `page` token of a list response's `next_page_url`.

    List methods request the next page by sending the same request again with
    this token, rather than by following the URL, because the API accepts a
    token only with the filters it was issued for and the URL can leave some
    out. Returns None on the last page.
    """
    if not next_page_url:
        return None
    tokens = parse_qs(urlsplit(next_page_url).query).get("page")
    return tokens[0] if tokens else None
