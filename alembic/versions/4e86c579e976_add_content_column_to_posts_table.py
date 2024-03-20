"""add content column to posts table

Revision ID: 4e86c579e976
Revises: 574826ca122b
Create Date: 2024-03-20 10:09:52.334074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e86c579e976'
down_revision: Union[str, None] = '574826ca122b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
