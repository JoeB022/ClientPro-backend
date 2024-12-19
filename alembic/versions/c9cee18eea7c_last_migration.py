"""last migration

Revision ID: c9cee18eea7c
Revises: aae95d0176f2
Create Date: 2024-12-19 23:06:50.959600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9cee18eea7c'
down_revision: Union[str, None] = 'aae95d0176f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
