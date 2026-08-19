"""add task confirmations

Revision ID: 5b49d0c93c4a
Revises: e9287708115a
Create Date: 2026-08-19 22:30:09.746832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b49d0c93c4a'
down_revision: Union[str, Sequence[str], None] = 'e9287708115a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "senior_confirmed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "tasks",
        sa.Column(
            "helper_confirmed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    op.drop_column("tasks", "helper_confirmed")
    op.drop_column("tasks", "senior_confirmed")