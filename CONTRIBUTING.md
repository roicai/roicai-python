# Contributing

This guide is for maintainers of the ROIC.ai Python library. To report a bug or request a feature, open a [GitHub issue](https://github.com/roicai/roicai-python/issues).

## Development

The package in `src/roicai` is generated from the API's OpenAPI document with [Fern](https://github.com/fern-api/fern). Don't edit the generated files by hand: CI regenerates them from `openapi.json` and fails on any difference.

These files are written by hand, and generation keeps them:

| File | What it does |
|---|---|
| `src/roicai/_version.py` | The package version, read by `pyproject.toml`, and the `User-Agent`. |
| `src/roicai/_paging.py` | Takes the `page` token from a response's `next_page_url`, so list methods request the next page with the same filters. |
| `src/roicai/_dataframe.py` | `to_pandas()` and `to_polars()` on every response and list. |
| `src/roicai/_errors.py` | The API's error fields on `ApiError` (`message`, `code`, `request_id`...), its message, pickling, and `error_body`, which keeps a non-JSON error body. |

The rest of the repository is also hand-written: `pyproject.toml`, the tests in `tests/` (except `tests/generated`), the scripts and this documentation.

Set up and test with [uv](https://docs.astral.sh/uv/):

```sh
uv sync --all-extras
uv run pytest                     # set ROICAI_API_KEY to also run the live tests
uv run ruff check . && uv run ruff format --check .
uv run mypy && uv run pyright
```

The live tests include `tests/test_readme.py`, which runs every Python example in `README.md` against the API. Keep the examples runnable: each runs on its own with `client`, `Roicai` and `httpx` defined.

## Regenerating the client

Generation needs Python 3.10+, Node.js (Fern's CLI runs with `npx`) and Docker (Fern runs its generator in a container). It needs no Fern account.

```sh
scripts/generate.sh               # from https://api.roic.ai/openapi.json
scripts/generate.sh ./spec.json   # from another document
scripts/generate.sh --committed   # from the committed openapi.json, as CI does
```

The script saves the API's document as `openapi.json`, then:

1. `scripts/prep_spec.py` writes the document Fern reads. It keeps the v3 operations, drops the `apikey` query parameter (the SDK sends the key as a bearer token), nests the dotted group names, adds Fern's pagination settings, and replaces the API's inlined objects with its named schemas, so types are `Ticker` rather than `V3TickerListDataItem`. It also turns numbers that the API's validator accepts as strings into plain numbers, and dates in responses into `datetime.date`.
2. Fern generates the package at the versions pinned in `fern/` (the CLI in `fern.config.json`, the Python generator in `generators.yml`).
3. `scripts/patch_generated.py` makes small changes to the generated code, listed at the top of the script: for example, it uses `_paging.py`, adds the mixins from `_dataframe.py` and `_errors.py`, retries streamed responses and adds `close()`. Each patch fails if the code it changes is missing, so a Fern upgrade can't drop one silently.
4. The script replaces `src/roicai` with the result, keeping the hand-written files, and updates `reference.md` and `tests/generated`.

The **Codegen** workflow does this after every API deploy and opens a pull request when the SDK changed. Review the `openapi.json` diff in that pull request: a removed or renamed method, group or field is a breaking change (see [Releasing](#releasing)).

### Upgrading Fern

Fern releases often. Change the versions in `fern/` in a pull request of their own, regenerate with `--committed`, and review the diff to the generated code. If a patch in `patch_generated.py` no longer applies, update it to the new code.

## Releasing

1. Open a pull request that sets `__version__` in `src/roicai/_version.py`. The SDK follows semver: while it is `0.x`, a breaking change needs a new minor version.
2. After it merges, publish a GitHub release whose tag is `v` plus that version, such as `v0.1.0`.

The **Release** workflow then tests, builds and publishes to PyPI with attestations, and attaches the files to the GitHub release. PyPI trusts that workflow, in the `pypi` environment, as the package's publisher, so there is no PyPI token to rotate.
