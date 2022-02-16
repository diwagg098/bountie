"""create users table

Revision ID: 5f9785fe7c8f
Revises: 
Create Date: 2021-11-04 15:39:38.658172

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '5f9785fe7c8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('password', sa.String(200), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('phone', sa.String(20)),
        sa.Column('fail_login', sa.Integer(), server_default='0'),
        sa.Column('registration_date', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column('last_login', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()),
        sa.Column('dob', sa.DateTime(timezone=True)),
    )


def downgrade():
    op.drop_table("users")
