"""Create admin level

Revision ID: b548296a98ea
Revises: 93557be37eeb
Create Date: 2021-12-24 08:33:30.901518

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import BOOLEAN


# revision identifiers, used by Alembic.
revision = 'b548296a98ea'
down_revision = '93557be37eeb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("is_admin", BOOLEAN, server_default="f"))


def downgrade():
    op.drop_column("users", "is_admin")
