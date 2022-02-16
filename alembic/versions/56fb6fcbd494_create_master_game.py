"""create master game

Revision ID: 56fb6fcbd494
Revises: b548296a98ea
Create Date: 2022-01-16 11:24:43.998453

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN

# revision identifiers, used by Alembic.
revision = '56fb6fcbd494'
down_revision = 'b548296a98ea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'games',
        sa.Column('id', UUID(), primary_key=True, server_default=text("uuid_generate_v4()")),
        sa.Column('image_url', sa.String(200), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(200)),
        sa.Column('featured', BOOLEAN, server_default="f")
    )


def downgrade():
    op.drop_table('games')
