"""Link lessons to modules

Revision ID: 9e4bb7c629b3
Revises: bcfb10fa67bc
Create Date: 2026-08-03 16:05:39.913110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4bb7c629b3'
down_revision: Union[str, Sequence[str], None] = 'bcfb10fa67bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add module_id as nullable first
    op.add_column(
        "lessons",
        sa.Column("module_id", sa.Integer(), nullable=True),
    )

    # 2. Create foreign key
    op.create_foreign_key(
        "lessons_module_id_fkey",
        "lessons",
        "modules",
        ["module_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 3. Remove old FK
    op.drop_constraint(
        "lessons_course_id_fkey",
        "lessons",
        type_="foreignkey",
    )

    # 4. Drop old column
    op.drop_column(
        "lessons",
        "course_id",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.add_column(
        "lessons",
        sa.Column("course_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "lessons_course_id_fkey",
        "lessons",
        "courses",
        ["course_id"],
        ["id"],
    )

    op.drop_constraint(
        "lessons_module_id_fkey",
        "lessons",
        type_="foreignkey",
    )

    op.drop_column(
        "lessons",
        "module_id",
    )
    # ### end Alembic commands ###
