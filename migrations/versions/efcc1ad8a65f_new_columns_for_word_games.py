"""new columns for word games

Revision ID: efcc1ad8a65f
Revises: 90dff69375cb
Create Date: 2020-04-24 23:43:11.074348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efcc1ad8a65f'
down_revision = '90dff69375cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_words', sa.Column('remember_word', sa.Integer(), nullable=True))
    op.add_column('users_words', sa.Column('translation_word', sa.Integer(), nullable=True))
    op.add_column('users_words', sa.Column('translation_write', sa.Integer(), nullable=True))
    op.add_column('users_words', sa.Column('word_write', sa.Integer(), nullable=True))
    op.alter_column('users_words', 'status',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_words', 'status',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users_words', 'word_write')
    op.drop_column('users_words', 'translation_write')
    op.drop_column('users_words', 'translation_word')
    op.drop_column('users_words', 'remember_word')
    # ### end Alembic commands ###