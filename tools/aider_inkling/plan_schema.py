"""Shared structured-output schema for V6 planning providers."""

PLAN_SCHEMA = {
    "type": "object",
    "required": ["schema_version", "objective", "analysis", "tasks"],
    "properties": {
        "schema_version": {"type": "string", "enum": ["inkling_plan_v6"]},
        "objective": {"type": "string"},
        "analysis": {
            "type": "object",
            "required": ["root_cause", "inspected_files"],
            "properties": {
                "root_cause": {"type": "string"},
                "inspected_files": {"type": "array", "items": {"type": "string"}},
            },
        },
        "tasks": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "id", "files", "target_symbols", "instruction",
                    "edits", "acceptance", "test_files",
                ],
                "properties": {
                    "id": {"type": "integer"},
                    "instruction": {"type": "string"},
                    **{
                        key: {"type": "array", "minItems": 1, "items": {"type": "string"}}
                        for key in ("files", "target_symbols", "acceptance", "test_files")
                    },
                    "edits": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 8,
                        "items": {
                            "type": "object",
                            "required": ["search", "replace"],
                            "properties": {
                                "search": {"type": "string"},
                                "replace": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
    },
}
