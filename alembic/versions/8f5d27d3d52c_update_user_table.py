"""Update user table

Revision ID: 8f5d27d3d52c
Revises: 2fd0081eb307
Create Date: 2021-12-23 04:42:30.889523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f5d27d3d52c'
down_revision = '2fd0081eb307'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("users", "first_name")
    op.drop_column("users", "last_name")
    op.add_column("users", sa.Column("name", sa.String(100), nullable=False))
    op.add_column("users", sa.Column("username", sa.String(100), unique=True))



def downgrade():
    op.add_column('first_name', sa.Column(sa.String(100), nullable=False))
    op.add_column('last_name', sa.Column(sa.String(100), nullable=False))
    op.drop_column("users", "name")
    op.drop_column("users", "username")
