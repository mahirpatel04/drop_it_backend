"""Added private column in User table

Revision ID: b169c0433bd8
Revises: 012d467ef9ef
Create Date: 2024-12-09 00:19:44.538700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b169c0433bd8'
down_revision: Union[str, None] = '012d467ef9ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('private', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'private')
    # ### end Alembic commands ###
