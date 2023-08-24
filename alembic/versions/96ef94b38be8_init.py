"""init

Revision ID: 96ef94b38be8
Revises:
Create Date: 2023-08-21 13:28:44.506046

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96ef94b38be8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # commands auto generated by Alembic - please adjust!
    op.create_table(
        "language_objects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("language_code", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_language_objects_id"), "language_objects", ["id"], unique=False
    )
    with open("alembic/default_data/language_objects.sql", "r") as file:
        dump = file.read()
    op.execute(dump)

    op.create_table(
        "telegram_channels",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_index(
        op.f("ix_telegram_channels_id"), "telegram_channels", ["id"], unique=False
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("fullname", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("language_code", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "association_users_channels",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("channel_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["channel_id"], ["telegram_channels.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "channel_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("association_users_channels")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_telegram_channels_id"), table_name="telegram_channels")
    op.drop_table("telegram_channels")
    op.drop_index(op.f("ix_language_objects_id"), table_name="language_objects")
    op.drop_table("language_objects")
    # ### end Alembic commands ###
