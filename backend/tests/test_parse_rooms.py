from __future__ import annotations

from app.rooms_txt import default_rooms_txt_path, parse_rooms_file, room_display_name


def test_parse_rooms_file() -> None:
    path = default_rooms_txt_path()
    rows = parse_rooms_file(path)
    assert len(rows) >= 1
    assert rows[0][0] == "4-028-14"
    assert "RF-Labor" in rows[0][1] or "Testber" in rows[0][1]


def test_room_display_name() -> None:
    assert room_display_name("4-028-15", "Büro") == "4-028-15 - Büro"
