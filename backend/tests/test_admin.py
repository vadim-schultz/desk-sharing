from __future__ import annotations

import jwt
from app.config import settings
from litestar import Litestar
from litestar.testing import TestClient


def _token(client: TestClient[Litestar]) -> str:
    r = client.post("/auth/token", json={"password": "wrong"})
    assert r.status_code == 401

    r = client.post("/auth/token", json={"password": "dresden"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert "access_token" in body
    assert body["expires_in"] > 0
    payload = jwt.decode(
        body["access_token"],
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload.get("scope") == "admin"
    return str(body["access_token"])


def test_admin_rooms_requires_auth(client: TestClient[Litestar]) -> None:
    r = client.get("/admin/rooms")
    assert r.status_code == 401


def test_admin_rooms_crud(client: TestClient[Litestar]) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get("/admin/rooms", headers=headers)
    assert r.status_code == 200
    assert r.json()["rooms"] == []

    create = client.post(
        "/admin/rooms",
        headers=headers,
        json={
            "room_number": "A-1",
            "description": "Test",
            "name": "A-1 - Test",
        },
    )
    assert create.status_code == 201, create.text
    room_id = create.json()["id"]

    r = client.get("/admin/rooms", headers=headers)
    assert len(r.json()["rooms"]) == 1

    desk = client.post(
        f"/admin/rooms/{room_id}/desks",
        headers=headers,
        json={
            "name": "Desk 1",
            "bookable": True,
            "monitor_count": 2,
            "has_keyboard": True,
            "has_mouse": False,
        },
    )
    assert desk.status_code == 201, desk.text
    desk_id = desk.json()["id"]

    patch_desk = client.patch(
        f"/admin/desks/{desk_id}",
        headers=headers,
        json={"monitor_count": 3, "has_mouse": True},
    )
    assert patch_desk.status_code == 200, patch_desk.text
    assert patch_desk.json()["monitor_count"] == 3
    assert patch_desk.json()["has_mouse"] is True

    del_desk = client.delete(f"/admin/desks/{desk_id}", headers=headers)
    assert del_desk.status_code == 204

    del_room = client.delete(f"/admin/rooms/{room_id}", headers=headers)
    assert del_room.status_code == 204

    r = client.get("/admin/rooms", headers=headers)
    assert r.json()["rooms"] == []
