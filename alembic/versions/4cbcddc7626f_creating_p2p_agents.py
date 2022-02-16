"""Creating p2p agents

Revision ID: 4cbcddc7626f
Revises: cf6830480f2e
Create Date: 2022-01-25 00:59:49.080659

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '4cbcddc7626f'
down_revision = 'cf6830480f2e'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
        "p2p_agents",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('name', sa.String(100)),
        sa.Column('phone', sa.String(100), unique=True),
        sa.Column('telegram', sa.String(100), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("country_code", sa.String(100), ForeignKey("countries.code")),
        sa.Column("active", sa.Boolean(), server_default="t")
    )


def downgrade():
    op.drop_table("p2p_agents")
