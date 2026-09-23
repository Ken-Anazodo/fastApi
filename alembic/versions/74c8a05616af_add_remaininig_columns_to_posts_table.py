"""add remaininig columns to posts table

Revision ID: 74c8a05616af
Revises: 40583b6ed86d
Create Date: 2026-09-23 11:30:49.845193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74c8a05616af'
down_revision: Union[str, None] = '40583b6ed86d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),) #This adds a new column called published to the posts table. It is set to be a boolean and it is set to be not nullable. This means that every post must have a published value. This is used to store whether the post is published or not.
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),) #This adds a new column called created_at to the posts table. It is set to be a timestamp and it is set to be not nullable. This means that every post must have a created_at value. This is used to store the timestamp of when the post was created.
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
