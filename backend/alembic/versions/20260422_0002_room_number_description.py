"""room number and description on rooms

Revision ID: 20260422_0002
Revises: 20260421_0001
Create Date: 2026-04-22

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260422_0002"
down_revision: Union[str, None] = "20260421_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("rooms", sa.Column("room_number", sa.String(length=64), nullable=True))
    op.add_column("rooms", sa.Column("description", sa.String(length=500), nullable=True))

    op.execute(sa.text("UPDATE rooms SET room_number = name WHERE room_number IS NULL"))
    op.execute(sa.text("UPDATE rooms SET description = '' WHERE description IS NULL"))

    op.alter_column("rooms", "room_number", existing_type=sa.String(length=64), nullable=False)
    op.alter_column("rooms", "description", existing_type=sa.String(length=500), nullable=False)
    op.alter_column(
        "rooms",
        "name",
        existing_type=sa.String(length=200),
        type_=sa.String(length=600),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "rooms",
        "name",
        existing_type=sa.String(length=600),
        type_=sa.String(length=200),
        existing_nullable=False,
    )
    op.drop_column("rooms", "description")
    op.drop_column("rooms", "room_number")
