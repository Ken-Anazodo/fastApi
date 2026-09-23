"""add foreign-key to posts table

Revision ID: 40583b6ed86d
Revises: 1cf22a48b6d8
Create Date: 2026-09-23 11:02:24.666110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40583b6ed86d'
down_revision: Union[str, None] = '1cf22a48b6d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE') #This creates a foreign key constraint on the posts table that references the users table. It is used to ensure that the owner_id column in the posts table references a valid id in the users table. It is used to ensure referential integrity between the posts and users tables. It is used to ensure that when a user is deleted, all of their posts are also deleted. It is used to ensure that when a user is deleted, all of their votes are also deleted.
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
