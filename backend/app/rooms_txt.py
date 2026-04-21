"""Parse `rooms.txt` lines: `room_number - description`."""

from __future__ import annotations

from pathlib import Path


def parse_rooms_file(path: Path) -> list[tuple[str, str]]:
    """Return (room_number, description) pairs in file order."""
    text = path.read_text(encoding="utf-8")
    rows: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if " - " not in line:
            continue
        number, desc = line.split(" - ", 1)
        number = number.strip()
        desc = desc.strip()
        if number and desc:
            rows.append((number, desc))
    return rows


def room_display_name(room_number: str, description: str) -> str:
    """Human-readable label (accordion title, sort key)."""
    return f"{room_number} - {description}"


def default_rooms_txt_path() -> Path:
    """`backend/scripts/rooms.txt` (repo layout)."""
    return Path(__file__).resolve().parent.parent / "scripts" / "rooms.txt"
