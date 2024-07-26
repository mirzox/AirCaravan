"""add fields for applications

Revision ID: 80393c07e48b
Revises: b3590bf6330c
Create Date: 2024-06-28 10:44:23.482689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80393c07e48b'
down_revision: Union[str, None] = 'b3590bf6330c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applications', sa.Column('operatorcode', sa.Integer, nullable=True))
    op.add_column('applications', sa.Column('operatorname', sa.String(200), nullable=True))
    op.add_column('applications', sa.Column('tourid', sa.String(200), nullable=True))


def downgrade() -> None:
    op.drop_column('applications', 'operatorcode')
    op.drop_column('applications', 'operatorname')
    op.drop_column('applications', 'tourid')
