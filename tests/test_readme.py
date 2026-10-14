"""Runs every Python example in README.md against the live API.

Skipped without ROICAI_API_KEY. Each example runs on its own, with `client`,
`Roicai` and `httpx` already defined, as the README's examples assume.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import httpx
import pytest

from roicai import Roicai

README = Path(__file__).resolve().parent.parent / "README.md"
EXAMPLES = re.findall(r"^```python\n(.*?)^```", README.read_text(), flags=re.DOTALL | re.MULTILINE)

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(not os.environ.get("ROICAI_API_KEY"), reason="needs ROICAI_API_KEY"),
]


def first_line(code: str) -> str:
    return next(line for line in code.splitlines() if line.strip() and not line.startswith(("import", "from")))


@pytest.mark.parametrize("code", EXAMPLES, ids=[first_line(c)[:60] for c in EXAMPLES])
@pytest.mark.filterwarnings("error::UserWarning")
def test_example(code: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    exec(
        compile(code, str(README), "exec"),
        {"client": Roicai(), "Roicai": Roicai, "httpx": httpx, "__name__": "__readme__"},
    )


def test_the_readme_has_examples() -> None:
    assert len(EXAMPLES) > 20
