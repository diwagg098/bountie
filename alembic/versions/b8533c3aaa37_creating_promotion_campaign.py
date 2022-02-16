"""Creating promotion campaign

Revision ID: b8533c3aaa37
Revises: 05e3bc016eae
Create Date: 2022-01-19 07:51:39.926572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN

# revision identifiers, used by Alembic.
revision = 'b8533c3aaa37'
down_revision = '05e3bc016eae'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "vouchers",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column("name", sa.String(200)),
        sa.Column("start_date", sa.DateTime(timezone=True)),
        sa.Column("end_date", sa.DateTime(timezone=True)),
        sa.Column("amount", sa.Integer()),
        sa.Column("max_amount", sa.Integer()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp())
    )
    op.create_table(
        "promotions",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column("name", sa.String(200)),
        sa.Column("start_date", sa.DateTime(timezone=True)),
        sa.Column("end_date", sa.DateTime(timezone=True)),
        sa.Column("banner_url", sa.String(200)),
        sa.Column("tnc", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("voucher_id", UUID(), ForeignKey("vouchers.id"), nullable=True),
    )


def downgrade():
    op.drop_table("promotions")
    op.drop_table("vouchers")
