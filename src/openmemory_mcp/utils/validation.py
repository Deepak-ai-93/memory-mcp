import re

PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/ -]{0,127}$")


def normalize_project(project: str) -> str:
    value = " ".join(project.strip().split())
    if not value or not PROJECT_RE.match(value):
        raise ValueError(
            "project must be 1-128 chars and contain only letters, numbers, space, _, -, ., :, /"
        )
    return value


def normalize_tags(tags: list[str] | None) -> list[str]:
    if not tags:
        return []
    cleaned: list[str] = []
    for tag in tags:
        value = tag.strip().lower()
        if value and value not in cleaned:
            cleaned.append(value[:64])
    return cleaned[:32]
