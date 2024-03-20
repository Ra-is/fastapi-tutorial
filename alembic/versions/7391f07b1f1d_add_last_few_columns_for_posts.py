"""add last few columns for posts

Revision ID: 7391f07b1f1d
Revises: cfe7f4d1e096
Create Date: 2024-03-20 11:02:50.713394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7391f07b1f1d'
down_revision: Union[str, None] = 'cfe7f4d1e096'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
      'published',sa.Boolean, nullable=False, server_default='True')),
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False))
      
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
