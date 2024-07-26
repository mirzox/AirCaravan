"""status column removed from applications

Revision ID: 620816b5b3d6
Revises: 14069b4fca3e
Create Date: 2024-06-24 16:48:50.440450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '620816b5b3d6'
down_revision: Union[str, None] = '14069b4fca3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_applications_status', table_name='applications')
    op.drop_column('applications', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applications', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_applications_status', 'applications', ['status'], unique=False)
    # ### end Alembic commands ###