"""UsersWords add column status

Revision ID: c6bb2c94f3eb
Revises: e0d14c97f4d2
Create Date: 2020-04-08 18:48:24.390351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6bb2c94f3eb'
down_revision = 'e0d14c97f4d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('teachers')
    op.add_column('users_words', sa.Column('status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_words', 'status')
    op.create_table('teachers',
    sa.Column('teacher_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('teacher_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('students',
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###