"""Adding countries

Revision ID: 2fd0081eb307
Revises: 5f9785fe7c8f
Create Date: 2021-11-05 06:30:18.541797

"""
from enum import unique
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '2fd0081eb307'
down_revision = '5f9785fe7c8f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'countries',
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('code', sa.String(100), nullable=False, unique=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('phone_code', sa.String(200), nullable=False),
    )

    op.add_column(
        "users",
        sa.Column("country_code", sa.String(100), ForeignKey("countries.code"))
    )


def downgrade():
    op.drop_table("countries")
    op.drop_column("users", "country_code")
