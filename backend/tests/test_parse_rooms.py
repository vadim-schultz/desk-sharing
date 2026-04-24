from __future__ import annotations

from app.rooms_txt import default_rooms_txt_path, parse_rooms_file, room_display_name


def test_parse_rooms_file() -> None:
    path = default_rooms_txt_path()
    rows = parse_rooms_file(path)
    assert len(rows) >= 1
    for number, desc in rows:
        assert number == number.strip()
        assert number
        assert desc == desc.strip()
        assert desc
    text = path.read_text(encoding="utf-8")
    first_data_line = next(
        ln.strip()
        for ln in text.splitlines()
        if ln.strip() and not ln.strip().startswith("#") and " - " in ln
    )
    num, description = first_data_line.split(" - ", 1)
    assert rows[0] == (num.strip(), description.strip())


def test_room_display_name() -> None:
    assert room_display_name("4-028-15", "Büro") == "4-028-15 - Büro"
