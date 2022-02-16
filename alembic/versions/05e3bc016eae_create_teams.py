"""Create teams

Revision ID: 05e3bc016eae
Revises: 56fb6fcbd494
Create Date: 2022-01-16 12:54:14.470939

"""
from time import timezone
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN

# revision identifiers, used by Alembic.
revision = '05e3bc016eae'
down_revision = '56fb6fcbd494'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "teams",
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("logo_url", sa.String(200)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column("deleted_at", sa.DateTime(timezone=True))
    )
    op.create_table(
        "team_members",
        sa.Column('user_id', UUID(), ForeignKey("users.id"), primary_key=True),
        sa.Column('team_id', UUID(), ForeignKey("teams.id"), primary_key=True)
    )


def downgrade():
    op.drop_table("teams")
    op.drop_table("team_members")