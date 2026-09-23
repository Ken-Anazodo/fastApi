"""creating posts table

Revision ID: 9cec94b2be7d
Revises: 
Create Date: 2026-09-22 15:25:15.621666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cec94b2be7d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), # alternatively for primary_key=True, we can use sa.PrimaryKeyConstraint('id') at the end of the table definition after listing all columns. This is used to tell Alembic that the id column is the primary key of the table.
    sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
