"""Turns the API's OpenAPI document into the one Fern generates the SDK from.

    python scripts/prep_spec.py openapi.json build/openapi.sdk.json

The API serves one document for every version. This keeps the v3 operations
and changes the document so the generated code reads well, without changing
what the SDK sends:

- The `apikey` query parameter is dropped: the SDK sends the key as a bearer
  token, named `api_key` and read from ROICAI_API_KEY.
- Dotted group names (`fundamentals.ratios`) become nested groups.
- List operations get Fern's pagination settings.
- Objects the API inlines are replaced with references to the named schemas
  they came from, so a list's items are `Ticker` rather than
  `V3TickerListDataItem`. Schema names lose their `v3.` prefix.
- Numbers that the API's validator also accepts as strings are plain numbers,
  and YYYY-MM-DD strings in responses are dates.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

PREFIX = "v3."
REF = "#/components/schemas/"
DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
METHODS = {"get", "post", "put", "patch", "delete"}
# Names for shared enums whose property name alone would be too vague.
ENUM_NAMES = {"status": "TickerStatus"}


def main(src: str, dst: str) -> None:
    with open(src) as f:
        doc = json.load(f)

    doc["paths"] = {p: item for p, item in doc["paths"].items() if p.startswith("/v3")}
    if not doc["paths"]:
        sys.exit("prep_spec: the document has no /v3 paths")

    schemes = doc["components"]["securitySchemes"]
    schemes.pop("apiKeyAuth", None)
    schemes["bearerAuth"]["x-fern-bearer"] = {"name": "api_key", "env": "ROICAI_API_KEY"}
    doc["security"] = [{"bearerAuth": []}]

    schemas = doc["components"]["schemas"]
    for name in list(schemas):
        if not name.startswith(PREFIX):
            del schemas[name]

    for op in operations(doc):
        op["security"] = [{"bearerAuth": []}]
        op["parameters"] = [p for p in op.get("parameters", []) if p.get("name") != "apikey"]
        group = op.get("x-fern-sdk-group-name")
        if isinstance(group, str):
            op["x-fern-sdk-group-name"] = group.split(".")
        if is_list(doc, op):
            op["x-fern-pagination"] = {
                "cursor": "$request.page",
                "next_cursor": "$response.next_page_url",
                "results": "$response.data",
            }

    for name, schema in schemas.items():
        schemas[name] = simplify(schema)
    for op in operations(doc):
        for param in op["parameters"]:
            # Parameters keep their dates as strings, such as "2024-01-01".
            param["schema"] = simplify(param["schema"], dates=False)
        for response in op.get("responses", {}).values():
            for media in response.get("content", {}).values():
                if "schema" in media:
                    media["schema"] = simplify(media["schema"])

    link_named_schemas(doc)
    name_list_items(doc)
    name_error_details(doc)
    prune(doc)
    rename(doc)
    name_shared_enums(doc)

    with open(dst, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")


def operations(doc: dict) -> list[dict]:
    return [
        op
        for item in doc["paths"].values()
        for method, op in item.items()
        if method in METHODS and isinstance(op, dict)
    ]


def resolve(doc: dict, schema: dict) -> dict:
    while "$ref" in schema:
        schema = doc["components"]["schemas"][schema["$ref"].removeprefix(REF)]
    return schema


def is_list(doc: dict, op: dict) -> bool:
    if not any(p.get("name") == "page" and p.get("in") == "query" for p in op["parameters"]):
        return False
    content = op.get("responses", {}).get("200", {}).get("content", {})
    schema = content.get("application/json", {}).get("schema")
    if schema is None:
        return False
    props = resolve(doc, schema).get("properties", {})
    return "data" in props and "next_page_url" in props


def simplify(schema: Any, dates: bool = True) -> Any:
    """Collapses numeric string unions and marks dates, recursively."""
    if isinstance(schema, list):
        return [simplify(s, dates) for s in schema]
    if not isinstance(schema, dict):
        return schema
    schema = {k: simplify(v, dates) for k, v in schema.items()}

    # The API's validator accepts "2024" as well as 2024 for numeric fields,
    # and the document says so with {anyOf: [{type: string, format: integer},
    # {type: integer}]}. The API always returns numbers, and the SDK sends them.
    # Booleans are the same, with "true" and "false" as the string forms.
    variants = schema.get("anyOf")
    if isinstance(variants, list) and len(variants) == 2:
        strings = [
            v
            for v in variants
            if v.get("type") == "string"
            and (v.get("format") in ("integer", "number", "numeric") or "[Tt][Rr][Uu][Ee]" in v.get("pattern", ""))
        ]
        typed = [v for v in variants if v.get("type") in ("integer", "number", "boolean")]
        if len(strings) == 1 and len(typed) == 1:
            merged = {k: v for k, v in schema.items() if k != "anyOf"}
            merged.update(typed[0])
            schema = merged
    if schema.get("type") in ("number", "integer") and schema.get("multipleOf") == 1:
        schema["type"] = "integer"
        del schema["multipleOf"]

    # A union of string constants is an enum, so it gets one type rather than
    # one per constant.
    variants = schema.get("anyOf")
    if isinstance(variants, list):
        consts = [v for v in variants if isinstance(v, dict) and "const" in v and v.get("type") == "string"]
        rest = [v for v in variants if v not in consts]
        if len(consts) > 1 and all(v == {"type": "null"} for v in rest):
            enum = {"type": "string", "enum": [v["const"] for v in consts]}
            schema["anyOf"] = [enum, *rest] if rest else None
            if not rest:
                del schema["anyOf"]
                schema.update(enum)

    # A nested union, such as anyOf [anyOf [integer], null] after the step
    # above, is flattened into one.
    if isinstance(schema.get("anyOf"), list):
        flat: list = []
        for v in schema["anyOf"]:
            if isinstance(v, dict) and list(v) == ["anyOf"]:
                flat.extend(v["anyOf"])
            else:
                flat.append(v)
        schema["anyOf"] = flat

    if dates and schema.get("type") == "string" and schema.get("pattern") == DATE_PATTERN:
        schema["format"] = "date"
    if schema.get("format") == "date":
        for key in ("pattern", "minLength", "maxLength"):
            schema.pop(key, None)
    return schema


def strip_ids(schema: Any) -> Any:
    if isinstance(schema, dict):
        return {k: strip_ids(v) for k, v in schema.items() if k != "$id"}
    if isinstance(schema, list):
        return [strip_ids(s) for s in schema]
    return schema


def link_named_schemas(doc: dict) -> None:
    """Replaces each inlined copy of a named schema with a reference to it.

    The API builds its schemas from shared objects, and the document repeats
    them inline, marked with the `$id` of the named schema they came from. A
    copy without the mark is matched by its content.
    """
    schemas = doc["components"]["schemas"]
    by_content = {}
    for name, schema in schemas.items():
        if schema.get("type") == "object" or "anyOf" in schema:
            by_content.setdefault(json.dumps(strip_ids(schema), sort_keys=True), name)

    def link(schema: Any, owner: str | None, root: bool) -> Any:
        if isinstance(schema, list):
            return [link(s, owner, False) for s in schema]
        if not isinstance(schema, dict):
            return schema
        if not root:
            target = None
            marked = schema.get("$id", "")
            if marked.startswith(REF) and marked.removeprefix(REF) in schemas:
                target = marked.removeprefix(REF)
            else:
                target = by_content.get(json.dumps(strip_ids(schema), sort_keys=True))
            if target is not None and target != owner:
                return {"$ref": REF + target}
        return {k: link(v, owner, False) for k, v in schema.items() if k != "$id"}

    for name in list(schemas):
        schemas[name] = link(schemas[name], name, True)
    for op in operations(doc):
        for response in op.get("responses", {}).values():
            for media in response.get("content", {}).values():
                if "schema" in media:
                    media["schema"] = link(media["schema"], None, True)


def name_list_items(doc: dict) -> None:
    """Gives each list's inline item schema a name: TickerList → Ticker."""
    schemas = doc["components"]["schemas"]
    for name in list(schemas):
        schema = schemas[name]
        items = schema.get("properties", {}).get("data", {}).get("items")
        if not name.endswith("List") or not isinstance(items, dict) or "$ref" in items:
            continue
        item_name = name.removesuffix("List")
        if item_name in schemas:
            item_name += "Item"
        schemas[item_name] = items
        schema["properties"]["data"]["items"] = {"$ref": REF + item_name}


def name_error_details(doc: dict) -> None:
    """Names the object inside an error body ErrorDetails, rather than ErrorError."""
    schemas = doc["components"]["schemas"]
    error = schemas[PREFIX + "Error"]["properties"]["error"]
    if "$ref" not in error:
        schemas[PREFIX + "ErrorDetails"] = error
        schemas[PREFIX + "Error"]["properties"]["error"] = {"$ref": REF + PREFIX + "ErrorDetails"}


def prune(doc: dict) -> None:
    """Drops named schemas no operation uses, such as the query models."""
    schemas = doc["components"]["schemas"]
    used: set[str] = set()

    def visit(schema: Any) -> None:
        if isinstance(schema, dict):
            ref = schema.get("$ref", "")
            if ref.startswith(REF) and ref.removeprefix(REF) not in used:
                used.add(ref.removeprefix(REF))
                visit(schemas[ref.removeprefix(REF)])
            for v in schema.values():
                visit(v)
        elif isinstance(schema, list):
            for v in schema:
                visit(v)

    visit(doc["paths"])
    for name in list(schemas):
        if name not in used:
            del schemas[name]


def rename(doc: dict) -> None:
    """Removes the v3. prefix from schema names and references."""
    schemas = doc["components"]["schemas"]
    names = {name: name.removeprefix(PREFIX) for name in schemas}
    if len(set(names.values())) != len(names):
        sys.exit("prep_spec: two schemas have the same name without the v3. prefix")
    doc["components"]["schemas"] = {names[n]: s for n, s in schemas.items()}
    text = json.dumps(doc)
    text = re.sub(
        r'"\$ref": "#/components/schemas/v3\.([^"]+)"',
        lambda m: f'"$ref": "{REF}{m.group(1)}"',
        text,
    )
    doc.clear()
    doc.update(json.loads(text))


def name_shared_enums(doc: dict) -> None:
    """Names each enum that several schemas or parameters share.

    `period_type` is the same three values on every statement, so it becomes
    one `PeriodType` rather than a type per statement and per request.
    """
    schemas = doc["components"]["schemas"]
    sites: dict[str, list[tuple[dict, str]]] = {}

    def enum_of(schema: Any) -> tuple | None:
        if isinstance(schema, dict) and schema.get("type") == "string" and "enum" in schema:
            return tuple(schema["enum"])
        return None

    def note(name: str, holder: dict, key: str) -> None:
        schema = holder[key]
        if enum_of(schema) is not None:
            sites.setdefault(name, []).append((holder, key))
        for i, variant in enumerate(schema.get("anyOf", []) if isinstance(schema, dict) else []):
            if enum_of(variant) is not None:
                sites.setdefault(name, []).append((schema["anyOf"], i))

    for schema in schemas.values():
        for prop in schema.get("properties", {}):
            note(prop, schema["properties"], prop)
    for op in operations(doc):
        for param in op["parameters"]:
            note(param["name"], param, "schema")

    for prop, found in sorted(sites.items()):
        values = {enum_of(holder[key]) for holder, key in found}
        name = ENUM_NAMES.get(prop) or "".join(p.capitalize() for p in re.split(r"[^A-Za-z0-9]+", prop) if p)
        if len(found) < 2 or len(values) != 1 or not name or name in schemas:
            continue
        schemas[name] = {"type": "string", "enum": list(values.pop())}
        for holder, key in found:
            extra = {k: v for k, v in holder[key].items() if k in ("description", "default")}
            holder[key] = {"$ref": REF + name, **extra}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
