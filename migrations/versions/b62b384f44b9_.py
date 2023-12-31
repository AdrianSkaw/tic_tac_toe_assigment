"""empty message

Revision ID: b62b384f44b9
Revises: f066a9b56cc7
Create Date: 2023-06-12 16:51:01.541455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b62b384f44b9'
down_revision = 'f066a9b56cc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('wins',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('ties',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('duration',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('duration',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
        batch_op.alter_column('ties',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('wins',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
