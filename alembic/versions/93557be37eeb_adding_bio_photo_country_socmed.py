"""Adding bio, photo, country, socmed

Revision ID: 93557be37eeb
Revises: ca259e1a3810
Create Date: 2021-12-24 05:02:29.198954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '93557be37eeb'
down_revision = 'ca259e1a3810'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("bio", sa.String(250)))
    op.add_column("users", sa.Column("photo_url", sa.String(250)))


def downgrade():
    op.drop_column("users", "bio")
    op.drop_column("users", "photo_url")
