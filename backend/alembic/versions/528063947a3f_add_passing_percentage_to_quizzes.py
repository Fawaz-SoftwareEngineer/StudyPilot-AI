"""add passing percentage to quizzes

Revision ID: 528063947a3f
Revises: bd5e4c3d8dab
Create Date: 2026-08-03 16:29:23.102919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '528063947a3f'
down_revision: Union[str, Sequence[str], None] = 'bd5e4c3d8dab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "quizzes",
        sa.Column(
            "passing_percentage",
            sa.Integer(),
            nullable=False,
            server_default="70",
        ),
    )

    # Optional: remove the server default after existing rows are populated.
    op.alter_column(
        "quizzes",
        "passing_percentage",
        server_default=None,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column("quizzes", "passing_percentage")
    # ### end Alembic commands ###
