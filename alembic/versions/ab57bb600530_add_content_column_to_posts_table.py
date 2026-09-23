"""add content column to posts table

Revision ID: ab57bb600530
Revises: 9cec94b2be7d
Create Date: 2026-09-23 01:15:41.123306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab57bb600530'
down_revision: Union[str, None] = '9cec94b2be7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False)) #This adds a new column called content to the posts table. It is set to be a string and it is set to be not nullable. This means that every post must have a content value. This is used to store the content of the post.
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content') #This drops the content column from the posts table. This is used to remove the content column from the posts table. This is used to undo the changes made in the upgrade function.
    pass
