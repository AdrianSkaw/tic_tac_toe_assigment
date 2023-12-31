"""changed game model

Revision ID: e6871fff80e0
Revises: dee46c10912e
Create Date: 2023-06-11 09:51:12.040870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6871fff80e0'
down_revision = 'dee46c10912e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('ties',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('game_player_name_fkey', type_='foreignkey')
        batch_op.drop_column('losses')
        batch_op.drop_column('wins')
        batch_op.drop_column('player_name')

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('symbol', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['symbol'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('symbol', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player_name', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('wins', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('losses', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('game_player_name_fkey', 'player', ['player_name'], ['name'])
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('ties',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
