"""Create unique constraints

Revision ID: ca259e1a3810
Revises: 8f5d27d3d52c
Create Date: 2021-12-23 08:22:15.016246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca259e1a3810'
down_revision = '8f5d27d3d52c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("uq_username_constraint", "users", ["username"])
    op.create_unique_constraint("uq_phone_constraint", "users", [ "phone"])
    op.create_unique_constraint("uq_email_constraint", "users", ["email"])


def downgrade():
    op.drop_constraint("uq_username_constraint", "users")
    op.drop_constraint("uq_phone_constraint", "users")
    op.drop_constraint("uq_email_constraint", "users")
