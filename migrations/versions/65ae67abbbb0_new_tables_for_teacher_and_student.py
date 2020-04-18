"""new tables for teacher and student

Revision ID: 65ae67abbbb0
Revises: a783a06f3ab1
Create Date: 2020-04-18 15:20:20.519274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65ae67abbbb0'
down_revision = 'a783a06f3ab1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('teachers',
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('teacher_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('teacher_student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.teacher_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_student')
    op.drop_table('teachers')
    op.drop_table('students')
    # ### end Alembic commands ###
