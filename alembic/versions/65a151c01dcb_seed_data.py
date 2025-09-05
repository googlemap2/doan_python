"""seed_data

Revision ID: 65a151c01dcb
Revises: 0b27ccf333ef
Create Date: 2025-09-05 11:14:04.652896

"""

from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Boolean, String, Integer, Text, BigInteger, DateTime


# revision identifiers, used by Alembic.
revision: str = "65a151c01dcb"
down_revision: Union[str, Sequence[str], None] = "0b27ccf333ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    brands_table = table("brands", column("id", Integer), column("name", String))

    users_table = table(
        "users",
        column("id", Integer),
        column("username", String),
        column("fullname", String),
        column("phone", String),
        column("address", String),
        column("password", String),
        column("created_at", DateTime),
        column("is_active", Boolean),
    )
    op.bulk_insert(
        brands_table,
        [
            {"id": 1, "name": "Apple"},
            {"id": 2, "name": "Samsung"},
            {"id": 3, "name": "Xiaomi"},
            {"id": 4, "name": "Oppo"},
            {"id": 5, "name": "Vivo"},
            {"id": 6, "name": "Huawei"},
            {"id": 7, "name": "OnePlus"},
            {"id": 8, "name": "Google"},
        ],
    )

    op.bulk_insert(
        users_table,
        [
            {
                "id": 1,
                "username": "admin",
                "fullname": "Administrator",
                "phone": "0987565139",
                "address": "ĐH UIT",
                "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiCdPu3eZxwa",
                "created_at": datetime.now(),
                "is_active": 1,
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM brands")
