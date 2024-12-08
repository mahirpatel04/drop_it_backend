"""changeduser model a bit

Revision ID: 62cd0b7d706f
Revises: 18bd63fcbe2f
Create Date: 2024-09-14 18:24:13.396005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62cd0b7d706f'
down_revision: Union[str, None] = '18bd63fcbe2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('drops', 'content',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=True))
    op.drop_index('ix_users_email_address', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.drop_column('users', 'email_address')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('email_address', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email_address', 'users', ['email_address'], unique=True)
    op.drop_column('users', 'email')
    op.alter_column('drops', 'content',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###
