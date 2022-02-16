"""Creating p2p listing

Revision ID: 655b2fe722de
Revises: 4cbcddc7626f
Create Date: 2022-01-25 02:38:28.544538

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '655b2fe722de'
down_revision = '4cbcddc7626f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tokens",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('symbol', sa.String(100), unique=True)
    )
    op.create_table(
        "p2p_listings",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('price', sa.Integer()),
        sa.Column('max_amount', sa.Integer()),
        sa.Column('payment_method', sa.String(100)),
        sa.Column('agent_id', UUID(), ForeignKey("p2p_agents.id")),
        sa.Column('token_symbol', sa.String(100), ForeignKey("tokens.symbol")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp())
    )


def downgrade():
    op.drop_table("p2p_listings")
    op.drop_table("tokens")
