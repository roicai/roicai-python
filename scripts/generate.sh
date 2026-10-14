#!/usr/bin/env bash
# Regenerates src/roicai from the ROIC.ai OpenAPI document.
#
#   scripts/generate.sh                  # fetch https://api.roic.ai/openapi.json
#   scripts/generate.sh path/or/url      # another document
#   scripts/generate.sh --committed      # the committed openapi.json, as CI checks
#
# Needs Python 3.10+, Node.js (for npx) and Docker. Fern runs its generator in
# Docker, at the versions pinned in fern/; it needs no Fern account.
set -euo pipefail

cd "$(dirname "$0")/.."
source="${1:-https://api.roic.ai/openapi.json}"
python="${PYTHON:-python3}"

# Files in src/roicai that are written by hand; generation keeps them.
hand_written=(_dataframe.py _errors.py _paging.py _version.py py.typed)

fetched="$(mktemp)"
trap 'rm -f "$fetched"' EXIT

if [[ "$source" == "--committed" ]]; then
  cp openapi.json "$fetched"
elif [[ "$source" == http* ]]; then
  curl -fsSL "$source" -o "$fetched"
else
  cp "$source" "$fetched"
fi

# An operation without SDK names would get a made-up name, and a document with
# none would replace every method.
"$python" - "$fetched" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
ops = [op for path, item in doc["paths"].items() if path.startswith("/v3") for op in item.values() if isinstance(op, dict)]
unnamed = [op.get("operationId", "?") for op in ops if "x-fern-sdk-group-name" not in op]
if not ops or unnamed:
    sys.exit(f"generate: v3 operations without x-fern-sdk-group-name: {unnamed or 'no operations'}")
json.dump(doc, open(sys.argv[1], "w"), indent=2, ensure_ascii=False)
open(sys.argv[1], "a").write("\n")
PY
cp "$fetched" openapi.json

rm -rf build
mkdir -p build
"$python" scripts/prep_spec.py openapi.json build/openapi.sdk.json

fern_version="$("$python" -c 'import json; print(json.load(open("fern/fern.config.json"))["version"])')"
# Fern asks before writing into a directory that has files; build/ is new.
npx --yes "fern-api@$fern_version" generate --local --log-level warn < /dev/null

"$python" scripts/patch_generated.py build/generated

# Replace the generated package, keeping the hand-written files.
keep="$(mktemp -d)"
for file in "${hand_written[@]}"; do
  [[ -e "src/roicai/$file" ]] && cp "src/roicai/$file" "$keep/"
done
rm -rf src/roicai tests/generated
mkdir -p src tests
mv build/generated/reference.md reference.md
mv build/generated/tests tests/generated
rm -rf build/generated/README.md build/generated/CONTRIBUTING.md build/generated/.fern
mv build/generated src/roicai
cp -a "$keep/." src/roicai/
rm -rf "$keep" build
