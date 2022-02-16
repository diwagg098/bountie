"""creating p2p customer list

Revision ID: cf6830480f2e
Revises: b8533c3aaa37
Create Date: 2022-01-23 05:21:40.341618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'cf6830480f2e'
down_revision = 'b8533c3aaa37'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "p2p_customers",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('name', sa.String(100)),
        sa.Column('phone', sa.String(100), unique=True),
        sa.Column('email', sa.String(100), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp())
    )


def downgrade():
    op.drop_table("p2p_customers")
