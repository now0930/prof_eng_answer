"""Apply the V6 line-aligned exact edit contract."""


def exact_patch(source, edits):
    if not isinstance(edits, list) or not edits:
        raise ValueError("edits must be a nonempty list")

    if len(edits) > 8:
        raise ValueError("too many edits in one task")

    output = source

    for edit in edits:
        old = edit["search"]
        new = edit["replace"]

        if not isinstance(old, str) or not isinstance(new, str):
            raise ValueError("edit blocks must be strings")

        if (
            not old.strip()
            or old == new
            or not old.endswith("\n")
            or not new.endswith("\n")
            or old.endswith("\n\n")
            or new.endswith("\n\n")
        ):
            raise ValueError("invalid or no-op edit")

        pos = output.find(old)

        if (
            pos < 0
            or (pos and output[pos - 1] != "\n")
            or output.find(old, pos + 1) >= 0
        ):
            raise ValueError("SEARCH must match exactly once")

        output = (
            output[:pos]
            + new
            + output[pos + len(old):]
        )

    if output == source:
        raise ValueError("net no-op")

    return output
