"""added imported_time to users_words

Revision ID: a783a06f3ab1
Revises: 6dc63bb63134
Create Date: 2020-04-07 20:46:51.137079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a783a06f3ab1'
down_revision = '6dc63bb63134'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_words', sa.Column('imported_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_words', 'imported_time')
    # ### end Alembic commands ###