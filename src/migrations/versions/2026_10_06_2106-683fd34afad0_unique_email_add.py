"""unique email add

Revision ID: 683fd34afad0
Revises: a9d17421a371
Create Date: 2026-10-06 21:06:22.263289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "683fd34afad0"
down_revision: Union[str, Sequence[str], None] = "a9d17421a371"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")

