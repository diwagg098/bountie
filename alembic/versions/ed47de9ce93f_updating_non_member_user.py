"""Updating non member user

Revision ID: ed47de9ce93f
Revises: 655b2fe722de
Create Date: 2022-02-03 09:53:48.300638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed47de9ce93f'
down_revision = '655b2fe722de'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("users", "password", nullable=True)



def downgrade():
    op.alter_column("users", "password", nullable=False)
