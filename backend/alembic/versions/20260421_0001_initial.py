"""initial schema

Revision ID: 20260421_0001
Revises:
Create Date: 2026-04-21

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260421_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "desks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("room_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("bookable", sa.Boolean(), nullable=False),
        sa.Column("monitor_count", sa.Integer(), nullable=False),
        sa.Column("has_keyboard", sa.Boolean(), nullable=False),
        sa.Column("has_mouse", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id", "name", name="uq_desks_room_name"),
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("desk_id", sa.Uuid(), nullable=False),
        sa.Column("booking_date", sa.Date(), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("checked_in_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["desk_id"], ["desks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("desk_id", "booking_date", name="uq_booking_desk_date"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
    op.drop_table("desks")
    op.drop_table("rooms")
